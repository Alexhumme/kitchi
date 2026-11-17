// Tarjeta del feed público del hub (P18).
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import CatSVG from './CatSVG';
import Avatar from './Avatar';
import type { PublicationRecord } from '../lib/types';

export default function FeedCard({ publication, index }: { publication: PublicationRecord; index: number }) {
  const cat = publication.cat;
  const title = publication.title || cat?.name || 'Sin título';
  return (
    <motion.article
      layout
      initial={{ opacity: 0, y: 26, scale: 0.92 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.9 }}
      transition={{ type: 'spring', stiffness: 380, damping: 30, delay: (index % 8) * 0.05 }}
      className="bevel-panel !rounded-[var(--radio-medio)] p-2"
      title={title}
    >
      <div className="feedcard__preview">
        <div className="feedcard__pattern" aria-hidden="true" />
        <CatSVG configuration={cat?.configuration} size={92} className="relative" />
      </div>
      <p className="mt-2 line-clamp-2 min-h-[2.1rem] px-1 text-[0.8rem] font-extrabold leading-snug text-[var(--ink)]">
        {title}
      </p>
      <Link
        to={`/publico/${encodeURIComponent(publication.author ?? '')}`}
        className="mb-1 mt-1 flex min-w-0 items-center gap-1.5 rounded-full px-1 py-0.5 transition-colors hover:bg-[var(--crema)]"
      >
        <Avatar name={publication.author ?? '?'} size={20} />
        <span className="truncate text-[0.72rem] font-bold text-[var(--tinta-suave)]">
          {publication.author ?? 'desconocido'}
        </span>
      </Link>
    </motion.article>
  );
}
