// Tarjeta de publicación del feed del hub (P18): cabecera con autor y hora,
// escenario con el gato, título/descripción y fila de acciones.
// Estructura basada en testui/feed.html con datos reales de la API.
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Cat, ChevronRight, PawPrint } from 'lucide-react';
import CatSVG from './CatSVG';
import Avatar from './Avatar';
import { timeAgo } from '../lib/format';
import { getOption, normalizeConfiguration } from '../lib/catalog';
import type { PublicationRecord } from '../lib/types';

export default function FeedCard({ publication, index }: { publication: PublicationRecord; index: number }) {
  const cat = publication.cat;
  const title = publication.title || cat?.name || 'Sin título';
  const description = publication.description?.trim();
  const navigate = useNavigate();
  const stageTint = ['amber', 'teal', 'lavender'][index % 3];

  const furCode = normalizeConfiguration(cat?.configuration).fur;
  const furName = getOption('fur', furCode)?.name ?? '';

  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 26, scale: 0.96 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.94 }}
      transition={{ type: 'spring', stiffness: 340, damping: 30, delay: (index % 6) * 0.06 }}
      className="postcard"
      title={title}
    >
      {/* cabecera: autor + hora + tipo */}
      <button
        type="button"
        className="postcard__head"
        onClick={() => navigate(`/publico/${encodeURIComponent(publication.author ?? '')}`)}
        aria-label={`Ver el perfil público de ${publication.author ?? 'la persona'}`}
      >
        <Avatar name={publication.author ?? '?'} size={28} />
        <span className="postcard__author-block">
          <span className="postcard__author">{publication.author ?? 'desconocido'}</span>
          <span className="postcard__time">{timeAgo(publication.created_at)}</span>
        </span>
        <span className="postcard__type">
          <Cat size={11} strokeWidth={2.6} aria-hidden="true" /> Gato
        </span>
      </button>

      {/* escenario */}
      <div className="postcard__stage" data-tint={stageTint}>
        <CatSVG configuration={cat?.configuration} size={118} className="postcard__cat" />
      </div>

      {/* cuerpo: título + descripción */}
      <div className="postcard__body">
        <div>
          <h2 className="postcard__title">{title}</h2>
          {description && <p className="postcard__desc">{description}</p>}
        </div>

        <div className="postcard__foot">
          {furName ? (
            <span className="postcard__fur">
              <PawPrint size={13} strokeWidth={2.5} aria-hidden="true" /> {furName}
            </span>
          ) : (
            <span />
          )}
          <button
            type="button"
            className="postcard__cta"
            onClick={() => navigate(`/publico/${encodeURIComponent(publication.author ?? '')}`)}
          >
            Ver gato <ChevronRight size={15} strokeWidth={3} aria-hidden="true" />
          </button>
        </div>
      </div>
    </motion.article>
  );
}
