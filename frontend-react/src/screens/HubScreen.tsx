// Navegar / Explorar: feed público del hub con buscador (P18).
import { useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { ArrowRight, CloudOff, Search, SearchX, Sparkles, X } from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import FeedCard from '../components/FeedCard';
import { EmptyState, SectionTitle } from '../components/ui';

export default function HubScreen() {
  const {
    publications, feedTotal, feedHasMore, feedQuery, feedSearching, feedError,
    setFeedQuery, loadMoreFeed, user, apiOnline,
  } = useKitchi();
  const navigate = useNavigate();

  return (
    <div className="screen-root">
      {/* encabezado */}
      <SectionTitle title="Explorar" subtitle="Creaciones de nuestra comunidad" />

      {/* buscador */}
      <label className="search-shell">
        <Search size={20} strokeWidth={2.4} className="search-shell__icon" aria-hidden="true" />
        <input
          type="search"
          className="search-shell__input"
          placeholder="Buscar creación o usuario…"
          value={feedQuery}
          onChange={(e) => setFeedQuery(e.target.value)}
          aria-label="Buscar en el hub"
        />
        {feedQuery && (
          <button type="button" className="search-shell__clear" onClick={() => setFeedQuery('')} aria-label="Limpiar búsqueda">
            <X size={18} strokeWidth={2.4} aria-hidden="true" />
          </button>
        )}
      </label>

      {/* contador + estado */}
      <div className="feed-meta">
        <p className="feed-count">
          {apiOnline
            ? `${feedTotal} publicación${feedTotal === 1 ? '' : 'es'} pública${feedTotal === 1 ? '' : 's'}`
            : 'Modo local: el hub necesita la API'}
        </p>
        <span className="badge badge--pink badge--flat">
          {feedSearching ? 'Actualizando…' : 'Actualizado'}
        </span>
      </div>

      {/* contenido */}
      {feedSearching && publications.length === 0 ? (
        <div className="feed-skeleton" aria-hidden="true">
          {[0, 1, 2, 3, 4, 5].map((n) => <div key={n} className="feed-skeleton__cell" />)}
        </div>
      ) : publications.length > 0 ? (
        <>
          <motion.div layout className="feed-grid">
            <AnimatePresence>
              {publications.map((pub, i) => (
                <FeedCard key={pub.id} publication={pub} index={i} />
              ))}
            </AnimatePresence>
          </motion.div>
          {feedHasMore && (
            <div className="load-more-row">
              <button type="button" className="bevel-btn load-more-btn" onClick={() => void loadMoreFeed()} disabled={feedSearching}>
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
            <button type="button" className="bevel-btn-coral" onClick={() => navigate('/crear')}>
              Crear mi gato <ArrowRight size={17} strokeWidth={2.6} />
            </button>
          }
        />
      )}
    </div>
  );
}
