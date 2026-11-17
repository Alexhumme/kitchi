// Mis gatos: lista de guardados (cuenta o navegador), publicar en el hub y eliminar.
import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { useKitchi, MAX_GUEST_CATS } from '../state/AppContext';
import CatSVG from '../components/CatSVG';
import Avatar from '../components/Avatar';
import { ConfirmDialog, EmptyState, SectionTitle } from '../components/ui';
import { ArrowRight, Cat, Check, Globe, Lock, Megaphone, Pencil, Trash } from 'lucide-react';
import type { CatRecord } from '../lib/types';

interface PublishTarget {
  cat: CatRecord;
}

export default function MyCatsScreen() {
  const {
    cats, user, deleteCat, restoreGuestCat, publishedCatIds, publishCat,
  } = useKitchi();
  const navigate = useNavigate();
  const [pendingDelete, setPendingDelete] = useState<CatRecord | null>(null);
  const [publishTarget, setPublishTarget] = useState<PublishTarget | null>(null);
  const [pubTitle, setPubTitle] = useState('');
  const [pubDescription, setPubDescription] = useState('');
  const [pubVisibility, setPubVisibility] = useState<'public' | 'private'>('public');
  const [publishing, setPublishing] = useState(false);
  const [lastDeleted, setLastDeleted] = useState<CatRecord | null>(null);

  useEffect(() => {
    if (!lastDeleted) return undefined;
    const t = window.setTimeout(() => setLastDeleted(null), 6000);
    return () => window.clearTimeout(t);
  }, [lastDeleted]);

  const guestCount = !user ? cats.length : 0;
  const isGuestFull = !user && cats.length >= MAX_GUEST_CATS;

  const openPublish = (cat: CatRecord) => {
    setPublishTarget({ cat });
    setPubTitle(cat.name);
    setPubDescription('');
    setPubVisibility('public');
  };

  const submitPublish = async () => {
    if (!publishTarget) return;
    const clean = pubTitle.trim();
    if (!clean) return;
    setPublishing(true);
    const ok = await publishCat(String(publishTarget.cat.id), clean, pubDescription.trim(), pubVisibility);
    setPublishing(false);
    if (ok) setPublishTarget(null);
  };

  const confirmDelete = async () => {
    if (!pendingDelete) return;
    const cat = pendingDelete;
    setPendingDelete(null);
    await deleteCat(cat);
    if (!user) setLastDeleted(cat);
  };

  const sorted = useMemo(
    () => [...cats].sort((a, b) => String(b.updated_at ?? '').localeCompare(String(a.updated_at ?? ''))),
    [cats],
  );

  return (
    <div className="app-scroll flex h-full flex-col gap-3 overflow-y-auto pr-1">
      <div className="flex items-start justify-between gap-2">
        <SectionTitle
          title="Mis gatos"
          subtitle={user ? 'Guardados en tu cuenta' : `Guardados en este navegador · ${guestCount}/${MAX_GUEST_CATS}`}
        />
        {isGuestFull && <span className="badge badge--warn shrink-0">Lleno</span>}
      </div>

      {!user && (
        <div className="flex shrink-0 items-center justify-between gap-3 rounded-2xl border-2 border-dashed border-[var(--tinta-suave)]/40 bg-[var(--superficie)]/60 px-4 py-2.5">
          <p className="text-[0.78rem] font-semibold leading-snug text-[var(--tinta-suave)]">
            Inicia sesión para publicar y sincronizar tus gatos.
          </p>
          <button type="button" className="bevel-btn-yellow shrink-0 px-3 py-1.5 text-xs" onClick={() => navigate('/auth/login')}>
            Entrar
          </button>
        </div>
      )}

      {sorted.length === 0 ? (
        <EmptyState
          icon={<Cat size={34} strokeWidth={2.1} />}
          title="Aún no tienes gatos"
          body="Entra en Crear, compón tu gato pieza por pieza y guárdalo. Después podrás publicarlo en el hub."
          action={
            <button type="button" className="bevel-btn-coral flex items-center gap-2 px-5 py-2.5 text-sm" onClick={() => navigate('/crear')}>
              Crear mi primer gato <ArrowRight size={17} strokeWidth={2.6} />
            </button>
          }
        />
      ) : (
        <div className="flex shrink-0 flex-col gap-2">
          <AnimatePresence>
            {sorted.map((cat) => {
              const published = publishedCatIds.has(String(cat.id));
              return (
                <motion.div
                  key={cat.id}
                  layout
                  initial={{ opacity: 0, x: -24 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: 40, transition: { duration: 0.18 } }}
                  transition={{ type: 'spring', stiffness: 380, damping: 32 }}
                  className="bevel-panel !rounded-[var(--radio-medio)] flex items-center gap-3 p-2.5"
                >
                  <div className="flex h-[72px] w-[64px] shrink-0 items-end justify-center overflow-hidden rounded-2xl bg-[var(--crema)]">
                    <CatSVG configuration={cat.configuration} size={54} />
                  </div>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-[0.95rem] font-extrabold text-[var(--ink)]">{cat.name}</p>
                    <p className="text-[0.68rem] font-semibold text-[var(--tinta-suave)]">
                      {cat.updated_at ? new Date(cat.updated_at).toLocaleDateString('es-CO', { day: 'numeric', month: 'short' }) : ''}
                      {published && ' · '}
                      {published && (
                        <span className="inline-flex items-center gap-0.5 font-extrabold text-[var(--menta-honda)]">
                          <Check size={12} strokeWidth={3.5} aria-hidden="true" /> Publicado
                        </span>
                      )}
                    </p>
                    <div className="mt-1.5 flex flex-wrap gap-1.5">
                      {user && !published && (
                        <button type="button" className="badge badge--pink !shadow-none hover:brightness-95" onClick={() => openPublish(cat)}>
                          <Megaphone size={13} strokeWidth={2.6} aria-hidden="true" /> Publicar
                        </button>
                      )}
                      <button type="button" className="badge badge--warn !shadow-none hover:brightness-95" onClick={() => navigate(`/crear?cat=${encodeURIComponent(String(cat.id))}`)}>
                        <Pencil size={13} strokeWidth={2.6} aria-hidden="true" /> Editar
                      </button>
                      <button type="button" className="badge badge--error !shadow-none hover:brightness-95" onClick={() => setPendingDelete(cat)}>
                        <Trash size={13} strokeWidth={2.6} aria-hidden="true" /> Eliminar
                      </button>
                    </div>
                  </div>
                </motion.div>
              );
            })}
          </AnimatePresence>
        </div>
      )}

      {/* deshacer eliminación (invitado) */}
      {lastDeleted && (
        <div className="fixed inset-x-4 bottom-24 z-30 flex items-center justify-between gap-3 rounded-2xl bg-[var(--ink)] px-4 py-3 text-[#fff] shadow-lg">
          <p className="text-[0.82rem] font-semibold">‘{lastDeleted.name}’ eliminado.</p>
          <button type="button" className="rounded-full bg-[var(--panel)] px-3 py-1.5 text-xs font-extrabold text-[var(--ink)]" onClick={() => { restoreGuestCat(lastDeleted); setLastDeleted(null); }}>
            Deshacer
          </button>
        </div>
      )}

      {/* diálogo de publicación */}
      {publishTarget && (
        <div className="absolute inset-0 z-40 flex items-end justify-center bg-black/45 backdrop-blur-[2px]" role="dialog" aria-modal="true" aria-label="Publicar gato">
          <motion.form
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            transition={{ type: 'spring', stiffness: 380, damping: 36 }}
            className="bevel-panel w-full !rounded-b-none p-5 pb-7"
            onSubmit={(e) => { e.preventDefault(); void submitPublish(); }}
          >
            <div className="flex items-center gap-3">
              <Avatar name={user?.username ?? '?'} size={40} />
              <div>
                <h2 className="text-base font-extrabold text-[var(--ink)]">Publicar a {user?.username}</h2>
                <p className="text-[0.7rem] font-semibold text-[var(--tinta-suave)]">Aparecerá en el feed público del hub</p>
              </div>
            </div>
            <label className="field-shell mt-4 block !rounded-[var(--radio-medio)] px-4 py-1">
              <span className="sr-only">Título</span>
              <input className="field-shell__input" value={pubTitle} onChange={(e) => setPubTitle(e.target.value)} maxLength={120} placeholder="Título de la publicación" autoFocus />
            </label>
            <label className="field-shell mt-2 block !rounded-[var(--radio-medio)] px-4 py-1">
              <span className="sr-only">Descripción</span>
              <textarea className="field-shell__input min-h-[64px] resize-none" value={pubDescription} onChange={(e) => setPubDescription(e.target.value)} maxLength={500} placeholder="Descripción breve (opcional)" />
            </label>
            <fieldset className="mt-3">
              <legend className="text-[0.72rem] font-extrabold uppercase tracking-wide text-[var(--tinta-suave)]">Visibilidad</legend>
              <div className="mt-1.5 flex gap-2">
                {(['public', 'private'] as const).map((v) => (
                  <button
                    key={v}
                    type="button"
                    className="bevel-chip flex-1 justify-center !py-2"
                    data-selected={pubVisibility === v}
                    onClick={() => setPubVisibility(v)}
                  >
                    {v === 'public' ? (
                      <><Globe size={15} strokeWidth={2.4} aria-hidden="true" /> Pública</>
                    ) : (
                      <><Lock size={15} strokeWidth={2.4} aria-hidden="true" /> Privada</>
                    )}
                  </button>
                ))}
              </div>
            </fieldset>
            <div className="mt-4 flex justify-end gap-2">
              <button type="button" className="bevel-btn px-4 py-2 text-sm font-extrabold" onClick={() => setPublishTarget(null)}>
                Cancelar
              </button>
              <button type="submit" className="bevel-btn-coral px-5 py-2 text-sm disabled:opacity-50" disabled={!pubTitle.trim() || publishing}>
                {publishing ? 'Publicando…' : 'Publicar'}
              </button>
            </div>
          </motion.form>
        </div>
      )}

      <ConfirmDialog
        open={Boolean(pendingDelete)}
        title="¿Eliminar este gato?"
        body={user
          ? `‘${pendingDelete?.name}’ se borrará de tu cuenta en el servidor.`
          : `‘${pendingDelete?.name}’ se borrará de este navegador. Podrás deshacerlo justo después.`}
        confirmLabel="Eliminar"
        danger
        onConfirm={() => void confirmDelete()}
        onCancel={() => setPendingDelete(null)}
      />
    </div>
  );
}
