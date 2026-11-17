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
    <div className="screen-root">
      <div className="editor-head">
        <SectionTitle
          title="Mis gatos"
          subtitle={user ? 'Guardados en tu cuenta' : `Guardados en este navegador · ${guestCount}/${MAX_GUEST_CATS}`}
        />
        {isGuestFull && <span className="badge badge--warn">Lleno</span>}
      </div>

      {!user && (
        <div className="guest-banner">
          <p className="guest-banner__text">
            Inicia sesión para publicar y sincronizar tus gatos.
          </p>
          <button type="button" className="bevel-btn-yellow btn-xs" onClick={() => navigate('/auth/login')}>
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
            <button type="button" className="bevel-btn-coral" onClick={() => navigate('/crear')}>
              Crear mi primer gato <ArrowRight size={17} strokeWidth={2.6} />
            </button>
          }
        />
      ) : (
        <div className="cat-list">
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
                  className="cat-card"
                >
                  <div className="cat-card__thumb">
                    <CatSVG configuration={cat.configuration} size={54} />
                  </div>
                  <div className="cat-card__body">
                    <p className="cat-card__name">{cat.name}</p>
                    <p className="cat-card__meta">
                      {cat.updated_at ? new Date(cat.updated_at).toLocaleDateString('es-CO', { day: 'numeric', month: 'short' }) : ''}
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
        </div>
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
