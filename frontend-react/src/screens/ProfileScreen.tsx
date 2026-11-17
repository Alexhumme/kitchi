// Perfil: identidad y sesión (cuenta o invitado).
import { useNavigate } from 'react-router-dom';
import { useKitchi, MAX_GUEST_CATS } from '../state/AppContext';
import Avatar from '../components/Avatar';
import { SectionTitle } from '../components/ui';
import { Cat, Crown, LogOut, Settings, ShieldCheck, ExternalLink } from 'lucide-react';

export default function ProfileScreen() {
  const { user, cats, logout } = useKitchi();
  const navigate = useNavigate();

  return (
    <div className="screen-root">
      {/* identidad */}
      <section className="identity-panel">
        <div className="identity-avatar-ring">
          <Avatar name={user?.username ?? 'Invitado'} size={64} />
        </div>
        <div className="identity-meta">
          <SectionTitle title={user?.username ?? 'Invitado'} />
          <p className="identity-email">
            {user?.email ?? 'Creando caos sin cuenta en este navegador'}
          </p>
          <div className="identity-chips">
            <span className="bevel-chip"><Cat size={14} strokeWidth={2.5} aria-hidden="true" /> {cats.length}{user ? '' : `/${MAX_GUEST_CATS}`} gatos</span>
            {user?.role && <span className="bevel-chip"><ShieldCheck size={14} strokeWidth={2.5} aria-hidden="true" /> {user.role}</span>}
            {user && <span className="bevel-chip"><Crown size={14} strokeWidth={2.5} aria-hidden="true" /> {user.premium ? 'Premium' : 'Plan gratuito'}</span>}
          </div>
        </div>
      </section>

      {user ? (
        <section className="session-panel">
          <SectionTitle title="Sesión activa" subtitle="Token de Django + permisos RBAC" />
          <p className="session-body">
            Sesión de {user.username}. Los gatos que guardes viajan a la API y el límite de
            tres se aplica en el backend.
          </p>
          {user.date_joined && (
            <p className="session-date">
              Miembro desde {new Date(user.date_joined).toLocaleDateString('es-CO', { day: 'numeric', month: 'long', year: 'numeric' })}
            </p>
          )}
          <button type="button" className="bevel-btn-coral btn-lg btn-block session-cta" onClick={() => void logout()}>
            <LogOut size={17} strokeWidth={2.5} /> Cerrar sesión
          </button>
        </section>
      ) : (
        <section className="session-panel">
          <SectionTitle title="Cuenta" subtitle="Registro e inicio de sesión" />
          <p className="session-body">
            Con una cuenta guardas tus gatos en el servidor, publicas en el hub y copias
            creaciones de otras personas. Tus gatos de invitado se migran automáticamente al entrar.
          </p>
          <div className="session-actions">
            <button type="button" className="bevel-btn-coral" onClick={() => navigate('/auth/register')}>
              Registrarse
            </button>
            <button type="button" className="bevel-btn" onClick={() => navigate('/auth/login')}>
              Iniciar sesión
            </button>
          </div>
        </section>
      )}

      <section className="shortcuts-panel">
        <SectionTitle title="Atajos" />
        <div className="shortcuts-grid">
          <button
            type="button"
            className="bevel-btn"
            disabled={!user}
            title={user ? 'Ver mi tarjeta pública' : 'Inicia sesión para ver tu perfil público'}
            onClick={() => user && navigate(`/publico/${encodeURIComponent(user.username)}`)}
          >
            <ExternalLink size={15} strokeWidth={2.5} /> Perfil público
          </button>
          <button type="button" className="bevel-btn" onClick={() => navigate('/settings')}>
            <Settings size={15} strokeWidth={2.5} /> Configuración
          </button>
        </div>
      </section>
    </div>
  );
}
