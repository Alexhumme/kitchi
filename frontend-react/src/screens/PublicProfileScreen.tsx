// Perfil público de un usuario (P18): gatos y publicaciones visibles.
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { ChevronLeft } from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import { api, ApiError } from '../lib/api';
import type { ProfileRecord } from '../lib/types';
import Avatar from '../components/Avatar';
import CatSVG from '../components/CatSVG';
import FeedCard from '../components/FeedCard';
import { EmptyState, SectionTitle } from '../components/ui';
import { CloudOff } from 'lucide-react';

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
            {[0, 1, 2, 3].map((n) => <div key={n} className="public-skeleton__cell" />)}
          </div>
        </div>
      ) : error ? (
        <EmptyState icon={<CloudOff size={34} strokeWidth={2.1} />} title="Perfil no disponible" body={error} />
      ) : profile ? (
        <>
          {/* cabecera */}
          <section className="public-header">
            <Avatar name={profile.username} size={64} />
            <div className="identity-meta">
              <h2 className="public-name">{profile.username}</h2>
              <p className="public-joined">
                {profile.joined_at ? `Miembro desde ${new Date(profile.joined_at).toLocaleDateString('es-CO', { day: 'numeric', month: 'long', year: 'numeric' })}` : 'Miembro'}
              </p>
              <span className="bevel-chip public-chip">{profile.publication_count} publicación{profile.publication_count === 1 ? '' : 'es'} pública{profile.publication_count === 1 ? '' : 's'}</span>
            </div>
          </section>

          {/* gatos publicados */}
          {profile.cats.length > 0 && (
            <section className="stickers-panel">
              <SectionTitle title="Gatos publicados" subtitle="Los que esta persona ha publicado en el hub" />
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
            <SectionTitle title="Publicaciones" subtitle={`${profile.publications.length} pública${profile.publications.length === 1 ? '' : 's'}`} />
            {profile.publications.length === 0 ? (
              <p className="public-count">Sin publicaciones públicas todavía.</p>
            ) : (
              <div className="public-pubs-grid">
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
