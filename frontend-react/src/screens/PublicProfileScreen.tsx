// Perfil público de un usuario (P18): gatos y publicaciones visibles.
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
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
    <div className="app-scroll flex h-full flex-col gap-3 overflow-y-auto pr-1">
      <header className="flex shrink-0 items-center gap-2 pt-1">
        <button type="button" className="grid h-10 w-10 place-items-center rounded-full text-[var(--ink)] hover:bg-black/5" onClick={() => navigate(-1)} aria-label="Volver">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><path d="M15 18l-6-6 6-6" /></svg>
        </button>
        <SectionTitle title="Perfil público" subtitle="Su huella pública en kitchi.studio" />
      </header>

      {loading ? (
        <div className="flex shrink-0 flex-col gap-3">
          <div className="h-24 animate-pulse rounded-[var(--radio-grande)] bg-[var(--crema-hondo)]" />
          <div className="grid grid-cols-2 gap-3">
            {[0, 1, 2, 3].map((n) => <div key={n} className="h-40 animate-pulse rounded-[var(--radio-medio)] bg-[var(--crema-hondo)]" />)}
          </div>
        </div>
      ) : error ? (
        <EmptyState icon={<CloudOff size={34} strokeWidth={2.1} />} title="Perfil no disponible" body={error} />
      ) : profile ? (
        <>
          {/* cabecera */}
          <section className="bevel-panel flex shrink-0 items-center gap-4 p-4">
            <Avatar name={profile.username} size={64} />
            <div className="min-w-0">
              <h2 className="truncate text-xl font-extrabold text-[var(--ink)]">{profile.username}</h2>
              <p className="text-[0.72rem] font-semibold text-[var(--tinta-suave)]">
                {profile.joined_at ? `Miembro desde ${new Date(profile.joined_at).toLocaleDateString('es-CO', { day: 'numeric', month: 'long', year: 'numeric' })}` : 'Miembro'}
              </p>
              <span className="bevel-chip mt-1">{profile.publication_count} publicación{profile.publication_count === 1 ? '' : 'es'} pública{profile.publication_count === 1 ? '' : 's'}</span>
            </div>
          </section>

          {/* gatos publicados */}
          {profile.cats.length > 0 && (
            <section className="bevel-panel shrink-0 p-4">
              <SectionTitle title="Gatos publicados" subtitle="Los que esta persona ha publicado en el hub" />
              <div className="mt-2 flex gap-2 overflow-x-auto pb-1">
                {profile.cats.map((cat) => (
                  <div key={cat.id} className="flex w-20 shrink-0 flex-col items-center gap-1 rounded-2xl bg-[var(--crema)] p-1.5" title={cat.name}>
                    <CatSVG configuration={cat.configuration} size={56} />
                    <span className="w-full truncate text-center text-[0.6rem] font-bold text-[var(--ink)]">{cat.name}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* publicaciones */}
          <section className="shrink-0 pb-1">
            <SectionTitle title="Publicaciones" subtitle={`${profile.publications.length} pública${profile.publications.length === 1 ? '' : 's'}`} />
            {profile.publications.length === 0 ? (
              <p className="mt-2 text-[0.82rem] font-semibold text-[var(--tinta-suave)]">Sin publicaciones públicas todavía.</p>
            ) : (
              <div className="mt-2 grid grid-cols-2 gap-3">
                {profile.publications.map((pub, i) => (
                  <FeedCard key={pub.id} publication={pub} index={i} />
                ))}
              </div>
            )}
          </section>
        </>
      ) : null}
      {!apiOnline && (
        <p className="shrink-0 text-center text-[0.7rem] font-semibold text-[var(--tinta-suave)]">La API no responde; los perfiles públicos necesitan conexión.</p>
      )}
    </div>
  );
}
