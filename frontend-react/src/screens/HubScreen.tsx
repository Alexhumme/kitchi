// Navegar / Explorar: río de publicaciones del hub con buscador y filtros (P18).
import { useNavigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import {
  ArrowRight, Cat, CloudOff, Flame, Package, Search, SearchX, Sparkles, Users, X, type LucideIcon,
} from 'lucide-react';
import { useState } from 'react';
import { useKitchi } from '../state/AppContext';
import FeedCard from '../components/FeedCard';
import { EmptyState, SectionTitle } from '../components/ui';

type FeedFilter = 'all' | 'cats';

const FILTERS: Array<{ key: FeedFilter | 'packs' | 'stickers' | 'creators'; label: string; icon: LucideIcon; soon?: boolean }> = [
  { key: 'all', label: 'Todo', icon: Flame },
  { key: 'cats', label: 'Gatos', icon: Cat },
  { key: 'packs', label: 'Packs de Stickers', icon: Package, soon: true },
  { key: 'stickers', label: 'Stickers sueltos', icon: Sparkles, soon: true },
  { key: 'creators', label: 'Creadores', icon: Users, soon: true },
];

export default function HubScreen() {
  const {
    publications, feedTotal, feedHasMore, feedQuery, feedSearching, feedError,
    setFeedQuery, loadMoreFeed, user, apiOnline,
  } = useKitchi();
  const navigate = useNavigate();
  const [filter, setFilter] = useState<FeedFilter>('all');

  return (
    <div className="screen-root">
      {/* encabezado */}
      <SectionTitle title="Explorar" subtitle="Creaciones de la comunidad" />

      {/* buscador */}
      <label className="search-shell">
        <Search size={20} strokeWidth={2.4} className="search-shell__icon" aria-hidden="true" />
        <input
          type="search"
          className="search-shell__input"
          placeholder="Buscar gato o creador…"
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

      {/* filtros del feed (los pendientes se marcan "pronto", no se simulan) */}
      <div className="filter-row no-scrollbar" role="tablist" aria-label="Filtrar el feed">
        {FILTERS.map((item) => {
          if (item.soon) {
            return (
              <button key={item.key} type="button" className="filter-chip" data-soon="true" disabled title="Muy pronto">
                <item.icon size={13} strokeWidth={2.4} aria-hidden="true" /> {item.label} <span className="filter-soon">Pronto</span>
              </button>
            );
          }
          const active = item.key === filter;
          return (
            <button
              key={item.key}
              type="button"
              role="tab"
              aria-selected={active}
              className="filter-chip"
              data-active={active}
              onClick={() => setFilter(item.key as FeedFilter)}
            >
              <item.icon size={13} strokeWidth={2.4} aria-hidden="true" /> {item.label}
            </button>
          );
        })}
      </div>

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
          {[0, 1, 2].map((n) => <div key={n} className="feed-skeleton__post" />)}
        </div>
      ) : publications.length > 0 ? (
        <>
          <div className="feed-stream">
            <AnimatePresence mode="popLayout">
              {publications.map((pub, i) => (
                <FeedCard key={pub.id} publication={pub} index={i} />
              ))}
            </AnimatePresence>
          </div>
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
