// Navegar / Explorar: feed público del hub con buscador (P18).
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { ArrowRight, CloudOff, Search, SearchX, Sparkles, X } from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import FeedCard from '../components/FeedCard';
import { EmptyState } from '../components/ui';

export default function HubScreen() {
  const {
    publications, feedTotal, feedHasMore, feedQuery, feedSearching, feedError,
    setFeedQuery, loadMoreFeed, user, apiOnline,
  } = useKitchi();
  const navigate = useNavigate();

  return (
    <div className="flex h-full flex-col gap-3 overflow-y-auto pr-1 app-scroll">
      {/* buscador */}
      <label className="field-shell flex shrink-0 items-center gap-2 !rounded-[var(--radio-pastilla)] px-4 py-1.5">
        <Search size={20} strokeWidth={2.4} className="shrink-0 text-[var(--tinta-suave)]" aria-hidden="true" />
        <input
          type="search"
          className="field-shell__input !py-2"
          placeholder="Buscar creación o usuario…"
          value={feedQuery}
          onChange={(e) => setFeedQuery(e.target.value)}
          aria-label="Buscar en el hub"
        />
        {feedQuery && (
          <button type="button" className="rounded-full p-1 text-[var(--tinta-suave)] hover:bg-black/5" onClick={() => setFeedQuery('')} aria-label="Limpiar búsqueda">
            <X size={18} strokeWidth={2.4} aria-hidden="true" />
          </button>
        )}
      </label>

      {/* contador + estado */}
      <div className="flex shrink-0 items-center justify-between gap-2">
        <p className="text-[0.72rem] font-semibold text-[var(--tinta-suave)]">
          {apiOnline
            ? `${feedTotal} publicación${feedTotal === 1 ? '' : 'es'} pública${feedTotal === 1 ? '' : 's'}`
            : 'Modo local: el hub necesita la API'}
        </p>
        <span className="badge badge--pink !shadow-none">
          {feedSearching ? 'Actualizando…' : 'Actualizado'}
        </span>
      </div>

      {/* contenido */}
      {feedSearching && publications.length === 0 ? (
        <div className="grid shrink-0 grid-cols-2 gap-3">
          {[0, 1, 2, 3, 4, 5].map((n) => (
            <div key={n} className="h-44 animate-pulse rounded-[var(--radio-medio)] bg-[var(--crema-hondo)]" />
          ))}
        </div>
      ) : publications.length > 0 ? (
        <>
          <motion.div layout className="grid shrink-0 grid-cols-2 gap-3">
            <AnimatePresence>
              {publications.map((pub, i) => (
                <FeedCard key={pub.id} publication={pub} index={i} />
              ))}
            </AnimatePresence>
          </motion.div>
          {feedHasMore && (
            <div className="flex shrink-0 justify-center pb-2">
              <button type="button" className="bevel-btn px-5 py-2.5 text-sm font-extrabold" onClick={() => void loadMoreFeed()} disabled={feedSearching}>
                {feedSearching ? 'Cargando…' : 'Cargar más ↓'}
              </button>
            </div>
          )}
        </>
      ) : feedError ? (
        <EmptyState icon={<CloudOff size={34} strokeWidth={2.1} />} title="Hub fuera de línea" body={feedError} />
      ) : feedQuery ? (
        <EmptyState icon={<SearchX size={34} strokeWidth={2.1} />} title="Nada por aquí" body={`Ninguna creación coincide con «${feedQuery}». Prueba con otro nombre o usuario.`} />
      ) : (
        <EmptyState
          icon={<Sparkles size={34} strokeWidth={2.1} />}
          title="El feed está por estrenarse"
          body={
            user
              ? 'Todavía no hay creaciones públicas. Publica un gato desde Mis gatos.'
              : 'Todavía no hay creaciones públicas. Crea un gato e inicia sesión para publicarlo.'
          }
          action={
            <button type="button" className="bevel-btn-coral flex items-center gap-2 px-5 py-2.5 text-sm" onClick={() => navigate('/crear')}>
              Crear mi gato <ArrowRight size={17} strokeWidth={2.6} />
            </button>
          }
        />
      )}
    </div>
  );
}
