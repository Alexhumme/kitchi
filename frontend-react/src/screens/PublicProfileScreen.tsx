// Perfil público de un usuario (P18): credencial con métricas,
// gatos y publicaciones visibles.
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ChevronLeft, Cat, SquareCheckBig, CloudOff } from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import { api, ApiError } from '../lib/api';
import type { ProfileRecord } from '../lib/types';
import Avatar from '../components/Avatar';
import CatSVG from '../components/CatSVG';
import FeedCard from '../components/FeedCard';
import { EmptyState, SectionTitle } from '../components/ui';
import { timeAgo } from '../lib/format';

function daysSince(iso?: string): number | null {
  if (!iso) return null;
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return null;
  return Math.max(1, Math.floor((Date.now() - then) / 86400000) + 1);
}

export default function PublicProfileScreen() {
  const { username = '' } = useParams<{ username: string }>();
  const navigate = useNavigate();
  const { apiOnline } = useKitchi();
  const [profile, setProfile] = useState<ProfileRecord | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    setError(null);
    void api.getPublicProfile(username)
      .then((data) => { if (!cancelled) { setProfile(data); setLoading(false); } })
      .catch((err) => {
        if (cancelled) return;
        setError(err instanceof ApiError ? err.userMessage() : 'No se pudo cargar el perfil.');
        setLoading(false);
      });
    return () => { cancelled = true; };
  }, [username]);

  const daysHere = profile ? daysSince(profile.joined_at) : null;

  return (
    <div className="screen-root">
      <header className="back-header">
        <button type="button" className="back-header__btn" onClick={() => navigate(-1)} aria-label="Volver">
          <ChevronLeft size={22} strokeWidth={2.4} />
        </button>
        <SectionTitle title="Perfil público" subtitle="Su huella pública en kitchi.studio" />
      </header>

      {loading ? (
        <div className="public-skeleton" aria-hidden="true">
          <div className="public-skeleton__header" />
          <div className="feed-skeleton">
            {[0, 1].map((n) => <div key={n} className="public-skeleton__cell" />)}
          </div>
        </div>
      ) : error ? (
        <EmptyState icon={<CloudOff size={34} strokeWidth={2.1} />} title="Perfil no disponible" body={error} />
      ) : profile ? (
        <>
          {/* credencial pública (solo datos públicos) */}
          <section className="credential-panel public-credential">
            <div className="credential-head">
              <div className="credential-avatar">
                <Avatar name={profile.username} size={64} />
              </div>
              <div className="credential-meta">
                <div className="credential-name-row">
                  <h1 className="credential-name">{profile.username}</h1>
                </div>
                <p className="credential-since">
                  {profile.joined_at
                    ? `En kitchi desde ${new Date(profile.joined_at).toLocaleDateString('es-CO', { day: 'numeric', month: 'long', year: 'numeric' })}`
                    : 'Miembro de la comunidad'}
                </p>
              </div>
            </div>
            <div className="metrics">
              <div className="metric">
                <span className="metric__num">{profile.cats.length}</span>
                <span className="metric__label">Gatos</span>
              </div>
              <div className="metric">
                <span className="metric__num">{profile.publication_count}</span>
                <span className="metric__label">Publicados</span>
              </div>
              <div className="metric">
                <span className="metric__num">{daysHere ?? '—'}</span>
                <span className="metric__label">Días aquí</span>
              </div>
            </div>
          </section>

          {/* gatos publicados */}
          {profile.cats.length > 0 && (
            <section className="public-cats-card">
              <h2 className="public-section-eyebrow">
                <Cat size={15} strokeWidth={2.5} aria-hidden="true" /> Gatos publicados
              </h2>
              <div className="public-cats-row">
                {profile.cats.map((cat) => (
                  <div key={cat.id} className="public-cat" title={cat.name}>
                    <CatSVG configuration={cat.configuration} size={56} />
                    <span className="public-cat__name">{cat.name}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* publicaciones */}
          <section className="public-pubs">
            <div className="public-pubs-head">
              <h2 className="public-section-eyebrow">
                <SquareCheckBig size={15} strokeWidth={2.5} aria-hidden="true" /> Publicaciones
              </h2>
              <span className="public-count-chip">
                {profile.publications.length} pública{profile.publications.length === 1 ? '' : 's'}
                {profile.publications[0]?.created_at ? ` · última ${timeAgo(profile.publications[0].created_at)}` : ''}
              </span>
            </div>
            {profile.publications.length === 0 ? (
              <p className="public-count">Sin publicaciones públicas todavía.</p>
            ) : (
              <div className="feed-stream public-pubs-grid">
                {profile.publications.map((pub, i) => (
                  <FeedCard key={pub.id} publication={pub} index={i} />
                ))}
              </div>
            )}
          </section>
        </>
      ) : null}
      {!apiOnline && (
        <p className="public-offline">La API no responde; los perfiles públicos necesitan conexión.</p>
      )}
    </div>
  );
}
