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
    <div className="app-scroll flex h-full flex-col gap-3 overflow-y-auto pr-1">
      {/* identidad */}
      <section className="bevel-panel flex shrink-0 items-center gap-4 p-4">
        <div className="rounded-full bg-[var(--panel)] p-1 shadow-[inset_-3px_-4px_0_0_var(--advertencia)]">
          <Avatar name={user?.username ?? 'Invitado'} size={64} />
        </div>
        <div className="min-w-0">
          <SectionTitle title={user?.username ?? 'Invitado'} />
          <p className="text-[0.78rem] font-semibold text-[var(--tinta-suave)]">
            {user?.email ?? 'Creando caos sin cuenta en este navegador'}
          </p>
          <div className="mt-1.5 flex flex-wrap gap-1.5">
            <span className="bevel-chip"><Cat size={14} strokeWidth={2.5} aria-hidden="true" /> {cats.length}{user ? '' : `/${MAX_GUEST_CATS}`} gatos</span>
            {user?.role && <span className="bevel-chip"><ShieldCheck size={14} strokeWidth={2.5} aria-hidden="true" /> {user.role}</span>}
            {user && <span className="bevel-chip"><Crown size={14} strokeWidth={2.5} aria-hidden="true" /> {user.premium ? 'Premium' : 'Plan gratuito'}</span>}
          </div>
        </div>
      </section>

      {user ? (
        <section className="bevel-panel shrink-0 p-4">
          <SectionTitle title="Sesión activa" subtitle="Token de Django + permisos RBAC" />
          <p className="mt-1.5 text-[0.85rem] font-medium leading-snug text-[var(--ink-soft)]">
            Sesión de {user.username}. Los gatos que guardes viajan a la API y el límite de
            tres se aplica en el backend.
          </p>
          {user.date_joined && (
            <p className="mt-1 text-[0.72rem] font-semibold text-[var(--tinta-suave)]">
              Miembro desde {new Date(user.date_joined).toLocaleDateString('es-CO', { day: 'numeric', month: 'long', year: 'numeric' })}
            </p>
          )}
          <button type="button" className="bevel-btn-coral mt-3 flex w-full items-center justify-center gap-2 py-3 text-sm" onClick={() => void logout()}>
            <LogOut size={17} strokeWidth={2.5} /> Cerrar sesión
          </button>
        </section>
      ) : (
        <section className="bevel-panel shrink-0 p-4">
          <SectionTitle title="Cuenta" subtitle="Registro e inicio de sesión" />
          <p className="mt-1.5 text-[0.85rem] font-medium leading-snug text-[var(--ink-soft)]">
            Con una cuenta guardas tus gatos en el servidor, publicas en el hub y copias
            creaciones de otras personas. Tus gatos de invitado se migran automáticamente al entrar.
          </p>
          <div className="mt-3 flex gap-2">
            <button type="button" className="bevel-btn-coral flex-1 py-2.5 text-sm" onClick={() => navigate('/auth/register')}>
              Registrarse
            </button>
            <button type="button" className="bevel-btn flex-1 px-3 py-2.5 text-sm font-extrabold" onClick={() => navigate('/auth/login')}>
              Iniciar sesión
            </button>
          </div>
        </section>
      )}

      <section className="bevel-panel shrink-0 p-4">
        <SectionTitle title="Atajos" />
        <div className="mt-2 grid grid-cols-2 gap-2">
          <button
            type="button"
            className="bevel-btn flex items-center justify-center gap-1.5 px-3 py-2.5 text-xs font-extrabold disabled:opacity-40"
            disabled={!user}
            title={user ? 'Ver mi tarjeta pública' : 'Inicia sesión para ver tu perfil público'}
            onClick={() => user && navigate(`/publico/${encodeURIComponent(user.username)}`)}
          >
            <ExternalLink size={15} strokeWidth={2.5} /> Perfil público
          </button>
          <button type="button" className="bevel-btn flex items-center justify-center gap-1.5 px-3 py-2.5 text-xs font-extrabold" onClick={() => navigate('/settings')}>
            <Settings size={15} strokeWidth={2.5} /> Configuración
          </button>
        </div>
      </section>
    </div>
  );
}
