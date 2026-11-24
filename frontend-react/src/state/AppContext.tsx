// Estado global de Kitchi Studio: sesión, gatos (cuenta o invitado),
// feed del hub y preferencias de la experiencia.
//
// Los gatos de invitado viven en localStorage bajo `kitchi.cats`.
// La sesión vive bajo `kitchi.session`. Las preferencias, bajo `kitchi.ui.*`.
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from 'react';
import { api, ApiError } from '../lib/api';
import { applyApiCatalog, normalizeConfiguration, toApiConfiguration, validateConfig } from '../lib/catalog';
import { syncFx } from '../lib/fx';
import type { CatRecord, PublicationRecord, UserRecord } from '../lib/types';

export interface Toast {
  id: number;
  text: string;
  tone: 'info' | 'success' | 'error' | 'warn';
}

const GUEST_CATS_KEY = 'kitchi.cats';
const SESSION_KEY = 'kitchi.session';
export const MAX_GUEST_CATS = 3;

const BUNDLED_POSES = [
  { code: 'greeting', name: 'Saludo' },
  { code: 'happy', name: 'Alegría' },
  { code: 'angry', name: 'Enfado' },
  { code: 'sad', name: 'Tristeza' },
  { code: 'surprised', name: 'Sorpresa' },
  { code: 'sleepy', name: 'Sueño' },
];

function nowIso(): string {
  return new Date().toISOString();
}

function newGuestCat(name: string, configuration: unknown): CatRecord {
  return {
    id: `local-${crypto.randomUUID().slice(0, 12)}`,
    name: name.trim(),
    configuration: configuration as Record<string, unknown>,
    created_at: nowIso(),
    updated_at: nowIso(),
  };
}

function normalizeCat(record: CatRecord): CatRecord {
  return {
    ...record,
    name: record.name?.trim() || 'Sin nombre',
    configuration: normalizeConfiguration(record.configuration) as unknown as Record<string, unknown>,
    created_at: record.created_at ?? nowIso(),
    updated_at: record.updated_at ?? nowIso(),
  };
}

function readGuestCats(): CatRecord[] {
  try {
    const raw = localStorage.getItem(GUEST_CATS_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as CatRecord[];
    if (!Array.isArray(parsed)) return [];
    return parsed.map(normalizeCat);
  } catch {
    return [];
  }
}

function writeGuestCats(cats: CatRecord[]): void {
  localStorage.setItem(GUEST_CATS_KEY, JSON.stringify(cats));
}

function readSession(): { token: string; user: UserRecord } | null {
  try {
    const raw = localStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    const parsed = JSON.parse(raw) as { token?: string; user?: UserRecord };
    if (!parsed.token || !parsed.user) return null;
    return { token: parsed.token, user: parsed.user };
  } catch {
    return null;
  }
}

function writeSession(token: string | null, user: UserRecord | null): void {
  if (token && user) localStorage.setItem(SESSION_KEY, JSON.stringify({ token, user }));
  else localStorage.removeItem(SESSION_KEY);
}

export interface KitchiContextValue {
  // conexión y arranque
  bootstrapping: boolean;
  apiOnline: boolean;
  apiError: string | null;
  catalogSource: 'bundled' | 'api';
  poses: Array<{ code: string; name: string }>;
  storageNotice: string | null;

  // sesión
  user: UserRecord | null;
  login: (mode: 'login' | 'register', username: string, email: string, password: string) => Promise<string | null>;
  logout: () => Promise<void>;

  // gatos
  cats: CatRecord[];
  refreshCats: (sessionToken?: string | null) => Promise<void>;
  saveCat: (name: string, configuration: unknown, editingId?: string | null) => Promise<CatRecord | null>;
  deleteCat: (cat: CatRecord) => Promise<void>;
  restoreGuestCat: (cat: CatRecord) => void;
  clearGuestCats: () => void;
  publishedCatIds: Set<string>;
  publishCat: (catId: string, title: string, description: string, visibility: 'public' | 'private') => Promise<boolean>;

  // hub / feed
  publications: PublicationRecord[];
  feedTotal: number;
  feedHasMore: boolean;
  feedQuery: string;
  feedSearching: boolean;
  feedError: string | null;
  setFeedQuery: (q: string) => void;
  loadMoreFeed: () => Promise<void>;
  refreshAll: () => Promise<void>;

  // preferencias
  soundEnabled: boolean;
  animationsEnabled: boolean;
  hapticsEnabled: boolean;
  setSoundEnabled: (v: boolean) => void;
  setAnimationsEnabled: (v: boolean) => void;
  setHapticsEnabled: (v: boolean) => void;

  // toasts
  toasts: Toast[];
  notify: (text: string, tone?: Toast['tone']) => void;
  dismissToast: (id: number) => void;
}

const KitchiContext = createContext<KitchiContextValue | null>(null);

let toastId = 0;

export function KitchiProvider({ children }: { children: ReactNode }) {
  const [bootstrapping, setBootstrapping] = useState(true);
  const [apiOnline, setApiOnline] = useState(false);
  const [apiError, setApiError] = useState<string | null>(null);
  const [catalogSource, setCatalogSource] = useState<'bundled' | 'api'>('bundled');
  const [poses, setPoses] = useState(BUNDLED_POSES);
  const [storageNotice, setStorageNotice] = useState<string | null>(null);

  const [user, setUser] = useState<UserRecord | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [cats, setCats] = useState<CatRecord[]>([]);
  const [publishedCatIds, setPublishedCatIds] = useState<Set<string>>(new Set());

  const [publications, setPublications] = useState<PublicationRecord[]>([]);
  const [feedTotal, setFeedTotal] = useState(0);
  const [feedPage, setFeedPage] = useState(1);
  const [feedHasMore, setFeedHasMore] = useState(false);
  const [feedQuery, setFeedQueryState] = useState('');
  const [feedSearching, setFeedSearching] = useState(false);
  const [feedError, setFeedError] = useState<string | null>(null);

  const [soundEnabled, setSoundEnabled] = useState(() => localStorage.getItem('kitchi.ui.sound') !== 'off');
  const [animationsEnabled, setAnimationsEnabled] = useState(() => localStorage.getItem('kitchi.ui.animations') !== 'off');
  const [hapticsEnabled, setHapticsEnabled] = useState(() => localStorage.getItem('kitchi.ui.haptic') !== 'off');

  const [toasts, setToasts] = useState<Toast[]>([]);
  const searchToken = useRef(0);

  const dismissToast = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const notify = useCallback((text: string, tone: Toast['tone'] = 'info') => {
    const id = ++toastId;
    setToasts((prev) => [...prev.slice(-2), { id, text, tone }]);
    window.setTimeout(() => dismissToast(id), 4200);
  }, [dismissToast]);

  // --- catálogo y conexión -------------------------------------------------
  const loadBackendCatalog = useCallback(async () => {
    try {
      const payload = await api.getCatalog();
      setApiOnline(true);
      setApiError(null);
      setCatalogSource(applyApiCatalog(payload) ? 'api' : 'bundled');
    } catch (err) {
      setApiOnline(false);
      setApiError(err instanceof ApiError ? err.userMessage() : 'La API no responde.');
      setCatalogSource('bundled');
    }
    try {
      const remotePoses = await api.getPoses();
      setPoses(remotePoses.length ? remotePoses : BUNDLED_POSES);
    } catch {
      setPoses(BUNDLED_POSES);
    }
  }, []);

  // --- feed ------------------------------------------------------------------
  const refreshFeed = useCallback(async (append: boolean, page: number, query: string) => {
    setFeedSearching(true);
    try {
      const data = await api.getPublications({ page, page_size: 12, q: query || undefined });
      const results = Array.isArray(data.results) ? data.results : [];
      setPublications((prev) => (append ? [...prev, ...results] : results));
      setFeedTotal(typeof data.count === 'number' ? data.count : results.length);
      setFeedHasMore(Boolean(data.next));
      setFeedPage(page);
      setFeedError(null);
    } catch (err) {
      const status = err instanceof ApiError ? err.status : null;
      setFeedError(
        status === 404 || status === 401
          ? 'El hub de publicaciones no está disponible en este momento.'
          : err instanceof ApiError
            ? err.userMessage()
            : 'El hub no está disponible en este momento.',
      );
    } finally {
      setFeedSearching(false);
    }
  }, []);

  const setFeedQuery = useCallback((q: string) => {
    const cleaned = q.trim();
    setFeedQueryState(cleaned);
    const token = ++searchToken.current;
    setFeedSearching(true);
    void (async () => {
      await new Promise((resolve) => setTimeout(resolve, 350));
      if (token !== searchToken.current) return;
      await refreshFeed(false, 1, cleaned);
    })();
  }, [refreshFeed]);

  const loadMoreFeed = useCallback(async () => {
    if (!feedHasMore || feedSearching) return;
    await refreshFeed(true, feedPage + 1, feedQuery);
  }, [feedHasMore, feedSearching, feedPage, feedQuery, refreshFeed]);

  // --- gatos ------------------------------------------------------------------
  const loadOwnPublications = useCallback(async (username: string) => {
    try {
      const data = await api.getPublications({ page: 1, page_size: 50, user: username });
      const results = Array.isArray(data.results) ? data.results : [];
      const ids = new Set<string>();
      for (const item of results) {
        const cid = item.cat?.id;
        if (cid !== undefined && cid !== null) ids.add(String(cid));
      }
      setPublishedCatIds(ids);
    } catch {
      setPublishedCatIds(new Set());
    }
  }, []);

  const refreshCats = useCallback(async (sessionToken?: string | null) => {
    const effectiveToken = sessionToken === undefined ? token : sessionToken;
    if (effectiveToken) {
      try {
        const records = await api.listCats();
        setCats(records.map((r) => normalizeCat(r)));
      } catch (err) {
        setCats([]);
        setApiError(err instanceof ApiError ? err.userMessage() : 'No se pudieron cargar los gatos.');
      }
      return;
    }
    try {
      setCats(readGuestCats());
      setStorageNotice(null);
    } catch {
      setCats([]);
      setStorageNotice('No se pudo abrir el almacenamiento de este navegador.');
    }
  }, [token]);

  const saveCat = useCallback(async (name: string, configuration: unknown, editingId?: string | null) => {
    const cleanName = name.trim();
    if (!cleanName) return null;
    const normalized = normalizeConfiguration(configuration);
    const errors = validateConfig(normalized);
    if (errors.length) {
      notify('La combinación no es válida para el catálogo actual.', 'error');
      return null;
    }
    const payload = toApiConfiguration(normalized);
    if (token) {
      try {
        if (editingId) {
          const record = await api.updateCat(editingId, { name: cleanName, configuration: payload } as Partial<CatRecord>);
          const cat = normalizeCat(record);
          setCats((prev) => prev.map((c) => (String(c.id) === String(cat.id) ? cat : c)));
          notify(`'${cat.name}' guardado en tu cuenta.`, 'success');
          return cat;
        }
        const record = await api.createCat(cleanName, payload);
        const cat = normalizeCat(record);
        setCats((prev) => [...prev, cat]);
        notify(`'${cat.name}' guardado en tu cuenta.`, 'success');
        return cat;
      } catch (err) {
        notify(err instanceof ApiError ? err.userMessage() : 'No se pudo guardar el gato.', 'error');
        return null;
      }
    }
    const existing = editingId ? cats.find((c) => String(c.id) === String(editingId)) : undefined;
    if (existing) {
      const updated: CatRecord = {
        ...existing,
        name: cleanName,
        configuration: payload,
        updated_at: nowIso(),
      };
      const next = cats.map((c) => (String(c.id) === String(editingId) ? updated : c));
      setCats(next);
      writeGuestCats(next);
      notify(`'${updated.name}' guardado en este navegador.`, 'success');
      return updated;
    }
    if (cats.length >= MAX_GUEST_CATS) {
      notify('Ya tienes 3 gatos. Elimina uno para guardar otro.', 'error');
      return null;
    }
    const cat = newGuestCat(cleanName, payload);
    const next = [...cats, cat];
    setCats(next);
    writeGuestCats(next);
    notify(`'${cat.name}' guardado en este navegador.`, 'success');
    return cat;
  }, [token, cats, notify]);

  const deleteCat = useCallback(async (cat: CatRecord) => {
    if (token) {
      try {
        await api.deleteCat(String(cat.id));
      } catch (err) {
        notify(err instanceof ApiError ? err.userMessage() : 'No se pudo eliminar el gato.', 'error');
        return;
      }
      setCats((prev) => prev.filter((c) => String(c.id) !== String(cat.id)));
      notify(`'${cat.name}' eliminado de tu cuenta.`, 'info');
      return;
    }
    const next = cats.filter((c) => String(c.id) !== String(cat.id));
    setCats(next);
    writeGuestCats(next);
    notify(`'${cat.name}' eliminado.`, 'info');
  }, [token, cats, notify]);

  const restoreGuestCat = useCallback((cat: CatRecord) => {
    setCats((prev) => {
      if (prev.length >= MAX_GUEST_CATS) return prev;
      const next = [...prev, normalizeCat(cat)];
      writeGuestCats(next);
      return next;
    });
    notify(`'${cat.name}' restaurado.`, 'success');
  }, [notify]);

  const clearGuestCats = useCallback(() => {
    setCats([]);
    writeGuestCats([]);
    notify('Datos de invitado vaciados.', 'info');
  }, [notify]);

  const publishCat = useCallback(async (catId: string, title: string, description: string, visibility: 'public' | 'private') => {
    try {
      await api.publishCat(catId, title, description, visibility);
      setPublishedCatIds((prev) => new Set(prev).add(String(catId)));
      notify('¡Publicado en el hub!', 'success');
      await refreshFeed(false, 1, feedQuery);
      return true;
    } catch (err) {
      notify(err instanceof ApiError ? err.userMessage() : 'No se pudo publicar el gato.', 'error');
      return false;
    }
  }, [notify, refreshFeed, feedQuery]);

  // --- sesión ------------------------------------------------------------------
  const login = useCallback(async (mode: 'login' | 'register', username: string, email: string, password: string) => {
    const guestCats = !user ? readGuestCats() : [];
    try {
      const data = mode === 'register'
        ? await api.register(username, email, password)
        : await api.login(username, password);
      const sessionToken = data.token;
      const sessionUser = (data.user as UserRecord) ?? { id: 0, username };
      api.setToken(sessionToken);
      setToken(sessionToken);
      setUser(sessionUser);
      writeSession(sessionToken, sessionUser);
      setApiOnline(true);
      setApiError(null);
      await loadBackendCatalog();
      const records = await api.listCats().catch(() => [] as CatRecord[]);
      const accountCats = records.map((r) => normalizeCat(r));
      setCats(accountCats);
      setFeedQueryState('');
      await refreshFeed(false, 1, '');
      await loadOwnPublications(sessionUser.username);

      // Migración de invitados: crea los gatos locales en la cuenta.
      if (guestCats.length) {
        const migratedIds: string[] = [];
        let working = [...accountCats];
        for (const guest of guestCats) {
          if (working.length >= MAX_GUEST_CATS + 100) break;
          try {
            const record = await api.createCat(guest.name, guest.configuration);
            working = [...working, normalizeCat(record)];
            migratedIds.push(String(guest.id));
          } catch {
            // deja el gato en localStorage si falla
          }
        }
        if (migratedIds.length) {
          setCats(working);
          writeGuestCats(readGuestCats().filter((g) => !migratedIds.includes(String(g.id))));
          notify(`${migratedIds.length} gato(s) de invitado pasaron a tu cuenta.`, 'success');
        }
      }
      notify(`Sesión iniciada como ${sessionUser.username}.`, 'success');
      return null;
    } catch (err) {
      return err instanceof ApiError ? err.userMessage() : 'No se pudo iniciar sesión.';
    }
  }, [user, loadBackendCatalog, refreshFeed, loadOwnPublications, notify]);

  const logout = useCallback(async () => {
    await api.logout();
    setToken(null);
    setUser(null);
    writeSession(null, null);
    setPublishedCatIds(new Set());
    try {
      setCats(readGuestCats());
    } catch {
      setCats([]);
    }
    setPublications([]);
    setFeedTotal(0);
    setFeedHasMore(false);
    setFeedPage(1);
    setFeedQueryState('');
    notify('Sesión cerrada. Vuelves al modo invitado.', 'info');
  }, [notify]);

  // --- preferencias -------------------------------------------------------------
  const setSound = useCallback((v: boolean) => {
    setSoundEnabled(v);
    localStorage.setItem('kitchi.ui.sound', v ? 'on' : 'off');
  }, []);
  const setAnimations = useCallback((v: boolean) => {
    setAnimationsEnabled(v);
    localStorage.setItem('kitchi.ui.animations', v ? 'on' : 'off');
    document.documentElement.dataset.animations = v ? 'on' : 'off';
  }, []);
  const setHaptics = useCallback((v: boolean) => {
    setHapticsEnabled(v);
    localStorage.setItem('kitchi.ui.haptic', v ? 'on' : 'off');
  }, []);

  const refreshAll = useCallback(async () => {
    await loadBackendCatalog();
    await refreshCats();
    await refreshFeed(false, 1, feedQuery);
    if (user) await loadOwnPublications(user.username);
    notify('Datos de la API actualizados.', 'success');
  }, [loadBackendCatalog, refreshCats, refreshFeed, feedQuery, loadOwnPublications, user, notify]);

  // --- sincroniza efectos (sonido/haptics) ---
  useEffect(() => {
    syncFx({ sound: soundEnabled, haptics: hapticsEnabled });
  }, [soundEnabled, hapticsEnabled]);

  // --- arranque -------------------------------------------------------------------
  useEffect(() => {
    let cancelled = false;
    void (async () => {
      const session = readSession();
      if (session) {
        api.setToken(session.token);
        try {
          const me = await api.me();
          if (!cancelled) {
            setToken(session.token);
            setUser(me);
          }
        } catch {
          api.setToken(null);
          writeSession(null, null);
          if (!cancelled) setApiError('La sesión guardada ya no es válida. Vuelve a entrar.');
        }
      }
      await loadBackendCatalog();
      if (cancelled) return;
      await refreshCats(session?.token ?? null);
      if (cancelled) return;
      await refreshFeed(false, 1, '');
      if (session) await loadOwnPublications(session.user.username);
      if (!cancelled) setBootstrapping(false);
    })();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const value = useMemo<KitchiContextValue>(() => ({
    bootstrapping,
    apiOnline,
    apiError,
    catalogSource,
    poses,
    storageNotice,
    user,
    login,
    logout,
    cats,
    refreshCats,
    saveCat,
    deleteCat,
    restoreGuestCat,
    clearGuestCats,
    publishedCatIds,
    publishCat,
    publications,
    feedTotal,
    feedHasMore,
    feedQuery,
    feedSearching,
    feedError,
    setFeedQuery,
    loadMoreFeed,
    refreshAll,
    soundEnabled,
    animationsEnabled,
    hapticsEnabled,
    setSoundEnabled: setSound,
    setAnimationsEnabled: setAnimations,
    setHapticsEnabled: setHaptics,
    toasts,
    notify,
    dismissToast,
  }), [
    bootstrapping, apiOnline, apiError, catalogSource, poses, storageNotice,
    user, login, logout, cats, refreshCats, saveCat, deleteCat, restoreGuestCat,
    clearGuestCats, publishedCatIds, publishCat,
    publications, feedTotal, feedHasMore, feedQuery, feedSearching, feedError,
    setFeedQuery, loadMoreFeed, refreshAll,
    soundEnabled, animationsEnabled, hapticsEnabled,
    setSound, setAnimations, setHaptics, toasts, notify, dismissToast,
  ]);

  return <KitchiContext.Provider value={value}>{children}</KitchiContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components
export function useKitchi(): KitchiContextValue {
  const ctx = useContext(KitchiContext);
  if (!ctx) throw new Error('useKitchi debe usarse dentro de <KitchiProvider>');
  return ctx;
}
