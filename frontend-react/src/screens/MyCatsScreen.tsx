// Mis gatos: colección de cartas de tus gatos con vista cuadrícula/lista,
// filtros Todos/Publicados/Borradores y acciones por tarjeta.
// Estructura basada en testui/misgatos.html.
import { useEffect, useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { useKitchi, MAX_GUEST_CATS } from '../state/AppContext';
import CatSVG from '../components/CatSVG';
import Avatar from '../components/Avatar';
import { ConfirmDialog, EmptyState } from '../components/ui';
import {
  ArrowRight, Cat, Check, Globe, LayoutGrid, List, Lock, Megaphone, MoreHorizontal, Pencil, Plus, Trash,
} from 'lucide-react';
import { getOption, normalizeConfiguration } from '../lib/catalog';
import type { CatRecord } from '../lib/types';

interface PublishTarget {
  cat: CatRecord;
}

const STAGE_TINTS = ['amber', 'teal', 'lavender'] as const;
type View = 'grid' | 'list';
type Filter = 'all' | 'published' | 'drafts';

function furName(cat: CatRecord): string {
  const cfg = normalizeConfiguration(cat.configuration);
  return getOption('fur', cfg.fur)?.name ?? '';
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
  const [view, setView] = useState<View>('grid');
  const [filter, setFilter] = useState<Filter>('all');
  const [openMenu, setOpenMenu] = useState<string | null>(null);

  useEffect(() => {
    if (!lastDeleted) return undefined;
    const t = window.setTimeout(() => setLastDeleted(null), 6000);
    return () => window.clearTimeout(t);
  }, [lastDeleted]);

  const guestFull = !user && cats.length >= MAX_GUEST_CATS;
  const guestRemaining = Math.max(0, MAX_GUEST_CATS - cats.length);

  const publishedCount = useMemo(
    () => cats.filter((c) => publishedCatIds.has(String(c.id))).length,
    [cats, publishedCatIds],
  );
  const draftCount = cats.length - publishedCount;

  const visibleCats = useMemo(() => {
    const sorted = [...cats].sort((a, b) => String(b.updated_at ?? '').localeCompare(String(a.updated_at ?? '')));
    if (filter === 'published') return sorted.filter((c) => publishedCatIds.has(String(c.id)));
    if (filter === 'drafts') return sorted.filter((c) => !publishedCatIds.has(String(c.id)));
    return sorted;
  }, [cats, filter, publishedCatIds]);

  const openPublish = (cat: CatRecord) => {
    setOpenMenu(null);
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

  const filterChips: Array<{ key: Filter; label: string; count: number }> = [
    { key: 'all', label: 'Todos', count: cats.length },
    { key: 'published', label: 'Publicados', count: publishedCount },
    { key: 'drafts', label: 'Borradores', count: draftCount },
  ];

  return (
    <div className="screen-root" onClick={() => setOpenMenu(null)}>
      {/* 2. encabezado: título + contador + toggle de vista */}
      <div className="mycats-head">
        <div className="mycats-head__titles">
          <h1 className="editor-title">Mis gatos</h1>
          <span className="mycats-count" aria-label={`${cats.length} gatos en la colección`}>{cats.length}</span>
        </div>
        <div className="view-toggle" role="group" aria-label="Cambiar vista">
          <button
            type="button"
            className="view-toggle__btn"
            data-active={view === 'grid'}
            onClick={() => setView('grid')}
            aria-pressed={view === 'grid'}
            title="Vista cuadrícula"
          >
            <LayoutGrid size={16} strokeWidth={2.4} />
          </button>
          <button
            type="button"
            className="view-toggle__btn"
            data-active={view === 'list'}
            onClick={() => setView('list')}
            aria-pressed={view === 'list'}
            title="Vista lista"
          >
            <List size={16} strokeWidth={2.4} />
          </button>
        </div>
      </div>

      {!user && (
        <div className="guest-banner">
          <p className="guest-banner__text">
            {guestFull
              ? 'Cupo lleno (3/3) en este navegador. Inicia sesión para publicar y sincronizar tus gatos.'
              : `Te quedan ${guestRemaining}/${MAX_GUEST_CATS} cupos en este navegador. Inicia sesión para publicar y sincronizar tus gatos.`}
          </p>
          <button type="button" className="bevel-btn-yellow btn-xs" onClick={() => navigate('/auth/login')}>
            Entrar
          </button>
        </div>
      )}

      {/* 3. filtros rápidos */}
      <div className="filter-row no-scrollbar" role="tablist" aria-label="Filtrar gatos">
        {filterChips.map((chip) => (
          <button
            key={chip.key}
            type="button"
            role="tab"
            aria-selected={filter === chip.key}
            className="filter-chip"
            data-active={filter === chip.key}
            onClick={() => setFilter(chip.key)}
          >
            {chip.key === 'published' && <span className="filter-dot" aria-hidden="true" />}
            {chip.label} ({chip.count})
          </button>
        ))}
      </div>

      {/* 4. contenido */}
      {cats.length === 0 ? (
        <EmptyState
          icon={<Cat size={34} strokeWidth={2.1} />}
          title="Aún no tienes gatos"
          body="Entra en Crear, compón tu gato pieza por pieza y guárdalo. Después podrás publicarlo en el hub."
          action={
            <button type="button" className="bevel-btn-coral" onClick={() => navigate('/crear')}>
              Crear mi primer gato <ArrowRight size={17} strokeWidth={2.6} />
            </button>
          }
        />
      ) : visibleCats.length === 0 ? (
        <p className="mycats-empty-filter">
          {filter === 'published' ? 'Ningún gato publicado todavía.' : 'Sin borradores por aquí.'}
        </p>
      ) : (
        <>
          {view === 'grid' ? (
            <div className="cats-grid">
              <AnimatePresence>
                {visibleCats.map((cat, i) => {
                  const published = publishedCatIds.has(String(cat.id));
                  const stageTint = STAGE_TINTS[i % STAGE_TINTS.length];
                  const date = cat.updated_at
                    ? new Date(cat.updated_at).toLocaleDateString('es-CO', { day: 'numeric', month: 'short' })
                    : '';
                  return (
                    <motion.article
                      key={cat.id}
                      layout
                      initial={{ opacity: 0, y: 18, scale: 0.92 }}
                      animate={{ opacity: 1, y: 0, scale: 1 }}
                      exit={{ opacity: 0, scale: 0.9 }}
                      transition={{ type: 'spring', stiffness: 380, damping: 32 }}
                      className="collectible"
                    >
                      {/* Escenario */}
                      <div className="collectible__stage" data-tint={stageTint}>
                        <span className={`collectible__badge ${published ? 'collectible__badge--ok' : 'collectible__badge--draft'}`}>
                          {published ? <><Check size={11} strokeWidth={4} aria-hidden="true" /> Público</> : 'Borrador'}
                        </span>
                        <button
                          type="button"
                          className="collectible__menu-btn"
                          aria-label={`Opciones para ${cat.name}`}
                          aria-expanded={openMenu === String(cat.id)}
                          onClick={(e) => { e.stopPropagation(); setOpenMenu(openMenu === String(cat.id) ? null : String(cat.id)); }}
                        >
                          <MoreHorizontal size={17} strokeWidth={2.4} />
                        </button>
                        {openMenu === String(cat.id) && (
                          <div className="collectible__menu" role="menu" onClick={(e) => e.stopPropagation()}>
                            {user && !published && (
                              <button type="button" className="collectible__menu-item" role="menuitem" onClick={() => openPublish(cat)}>
                                <Megaphone size={15} strokeWidth={2.4} aria-hidden="true" /> Publicar
                              </button>
                            )}
                            <button type="button" className="collectible__menu-item" role="menuitem" onClick={() => navigate(`/crear?cat=${encodeURIComponent(String(cat.id))}`)}>
                              <Pencil size={15} strokeWidth={2.4} aria-hidden="true" /> Editar
                            </button>
                            <button type="button" className="collectible__menu-item collectible__menu-item--danger" role="menuitem" onClick={() => { setOpenMenu(null); setPendingDelete(cat); }}>
                              <Trash size={15} strokeWidth={2.4} aria-hidden="true" /> Eliminar
                            </button>
                          </div>
                        )}
                        <CatSVG configuration={cat.configuration} size={104} className="collectible__cat" />
                      </div>

                      {/* Info + acción */}
                      <div className="collectible__info">
                        <div>
                          <h2 className="collectible__name">{cat.name}</h2>
                          <p className="collectible__meta">{date}{furName(cat) ? ` · ${furName(cat)}` : ''}</p>
                        </div>
                        <button type="button" className="collectible__edit" onClick={() => navigate(`/crear?cat=${encodeURIComponent(String(cat.id))}`)}>
                          <Pencil size={14} strokeWidth={2.5} aria-hidden="true" /> Editar
                        </button>
                      </div>
                    </motion.article>
                  );
                })}
              </AnimatePresence>

              {/* 5. hueco punteado: crear otro */}
              <button
                type="button"
                className="new-slot"
                onClick={() => navigate('/crear')}
                disabled={guestFull}
                title={guestFull ? 'Cupo lleno (3/3). Elimina uno para crear otro.' : 'Diseña un nuevo personaje para tu colección'}
              >
                <span className="new-slot__icon">
                  <Plus size={21} strokeWidth={2.8} aria-hidden="true" />
                </span>
                <span className="new-slot__text">
                  <span className="new-slot__title">{guestFull ? 'Cupo lleno (3/3)' : 'Crear otro gato'}</span>
                  <span className="new-slot__hint">{guestFull ? 'Elimina uno para crear otro' : 'Diseña un nuevo personaje para tu colección'}</span>
                </span>
              </button>
            </div>
          ) : (
            <div className="cat-list">
              <AnimatePresence>
                {visibleCats.map((cat) => {
                  const published = publishedCatIds.has(String(cat.id));
                  return (
                    <motion.div
                      key={cat.id}
                      layout
                      initial={{ opacity: 0, x: -24 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: 40, transition: { duration: 0.18 } }}
                      transition={{ type: 'spring', stiffness: 380, damping: 32 }}
                      className="cat-card"
                    >
                      <div className="cat-card__thumb">
                        <CatSVG configuration={cat.configuration} size={54} />
                      </div>
                      <div className="cat-card__body">
                        <p className="cat-card__name">{cat.name}</p>
                        <p className="cat-card__meta">
                          {cat.updated_at ? new Date(cat.updated_at).toLocaleDateString('es-CO', { day: 'numeric', month: 'short' }) : ''}
                          {furName(cat) ? ` · ${furName(cat)}` : ''}
                          {published && ' · '}
                          {published && (
                            <span className="cat-card__published">
                              <Check size={12} strokeWidth={3.5} aria-hidden="true" /> Publicado
                            </span>
                          )}
                        </p>
                        <div className="cat-card__actions">
                          {user && !published && (
                            <button type="button" className="badge badge--pink badge--flat badge--interactive" onClick={() => openPublish(cat)}>
                              <Megaphone size={13} strokeWidth={2.6} aria-hidden="true" /> Publicar
                            </button>
                          )}
                          <button type="button" className="badge badge--warn badge--flat badge--interactive" onClick={() => navigate(`/crear?cat=${encodeURIComponent(String(cat.id))}`)}>
                            <Pencil size={13} strokeWidth={2.6} aria-hidden="true" /> Editar
                          </button>
                          <button type="button" className="badge badge--error badge--flat badge--interactive" onClick={() => setPendingDelete(cat)}>
                            <Trash size={13} strokeWidth={2.6} aria-hidden="true" /> Eliminar
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  );
                })}
              </AnimatePresence>

              {/* hueco punteado como cierre de la lista */}
              <button
                type="button"
                className="new-slot new-slot--row"
                onClick={() => navigate('/crear')}
                disabled={guestFull}
              >
                <span className="new-slot__icon">
                  <Plus size={21} strokeWidth={2.8} aria-hidden="true" />
                </span>
                <span className="new-slot__text">
                  <span className="new-slot__title">{guestFull ? 'Cupo lleno (3/3)' : 'Crear otro gato'}</span>
                  <span className="new-slot__hint">{guestFull ? 'Elimina uno para crear otro' : 'Diseña un nuevo personaje'}</span>
                </span>
              </button>
            </div>
          )}
        </>
      )}

      {/* deshacer eliminación (invitado) */}
      {lastDeleted && (
        <div className="undo-bar">
          <p className="undo-bar__text">‘{lastDeleted.name}’ eliminado.</p>
          <button type="button" className="undo-bar__action" onClick={() => { restoreGuestCat(lastDeleted); setLastDeleted(null); }}>
            Deshacer
          </button>
        </div>
      )}

      {/* diálogo de publicación */}
      {publishTarget && (
        <div className="publish-overlay" role="dialog" aria-modal="true" aria-label="Publicar gato">
          <motion.form
            initial={{ y: '100%' }}
            animate={{ y: 0 }}
            transition={{ type: 'spring', stiffness: 380, damping: 36 }}
            className="publish-panel"
            onSubmit={(e) => { e.preventDefault(); void submitPublish(); }}
          >
            <div className="publish-head">
              <Avatar name={user?.username ?? '?'} size={40} />
              <div className="publish-head-text">
                <h2 className="publish-title">Publicar a {user?.username}</h2>
                <p className="publish-subtitle">Aparecerá en el feed público del hub</p>
              </div>
            </div>
            <div className="publish-form">
              <label className="field-shell">
                <span className="sr-only">Título</span>
                <input className="field-shell__input" value={pubTitle} onChange={(e) => setPubTitle(e.target.value)} maxLength={120} placeholder="Título de la publicación" autoFocus />
              </label>
              <label className="field-shell">
                <span className="sr-only">Descripción</span>
                <textarea className="field-shell__input field-shell__input--area" value={pubDescription} onChange={(e) => setPubDescription(e.target.value)} maxLength={500} placeholder="Descripción breve (opcional)" />
              </label>
              <fieldset className="publish-visibility">
                <legend className="publish-legend">Visibilidad</legend>
                <div className="publish-visibility-row">
                  {(['public', 'private'] as const).map((v) => (
                    <button
                      key={v}
                      type="button"
                      className="bevel-chip"
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
              <div className="publish-actions">
                <button type="button" className="bevel-btn" onClick={() => setPublishTarget(null)}>
                  Cancelar
                </button>
                <button type="submit" className="bevel-btn-coral" disabled={!pubTitle.trim() || publishing}>
                  {publishing ? 'Publicando…' : 'Publicar'}
                </button>
              </div>
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
