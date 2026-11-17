// Tarjeta del feed público del hub (P18).
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import CatSVG from './CatSVG';
import Avatar from './Avatar';
import type { PublicationRecord } from '../lib/types';

export default function FeedCard({ publication, index }: { publication: PublicationRecord; index: number }) {
  const cat = publication.cat;
  const title = publication.title || cat?.name || 'Sin título';
  const navigate = useNavigate();
  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 26, scale: 0.92 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ type: 'spring', stiffness: 380, damping: 30, delay: (index % 8) * 0.05 }}
      className="feedcard"
      title={title}
    >
      <div className="feedcard__preview">
        <div className="feedcard__pattern" aria-hidden="true" />
        <CatSVG configuration={cat?.configuration} size={92} className="feedcard__cat" />
      </div>
      <p className="feedcard__title">{title}</p>
      <button
        type="button"
        className="feedcard__author"
        onClick={() => navigate(`/publico/${encodeURIComponent(publication.author ?? '')}`)}
      >
        <Avatar name={publication.author ?? '?'} size={20} />
        <span className="feedcard__author-name">{publication.author ?? 'desconocido'}</span>
      </button>
    </motion.article>
  );
}
