// Perfil: credencial con métricas reales, tarjeta de plan y capacidad,
// y accesos (cuenta, configuración, sesión).
// Estructura basada en testui/miperfil.html.
import { useNavigate } from 'react-router-dom';
import { useKitchi, MAX_GUEST_CATS } from '../state/AppContext';
import Avatar from '../components/Avatar';
import { Cat, Check, Crown, ExternalLink, LogOut, Settings, ShieldCheck, Sparkles, UserRoundPlus } from 'lucide-react';

function daysSince(iso?: string): number | null {
  if (!iso) return null;
  const then = new Date(iso).getTime();
  if (Number.isNaN(then)) return null;
  return Math.max(1, Math.floor((Date.now() - then) / 86400000) + 1);
}

export default function ProfileScreen() {
  const { user, cats, logout, publishedCatIds } = useKitchi();
  const navigate = useNavigate();

  const publishedCount = cats.filter((c) => publishedCatIds.has(String(c.id))).length;
  const daysHere = user ? daysSince(user.date_joined) : null;
  const isAdmin = user?.role === 'admin';
  const count = Math.min(cats.length, MAX_GUEST_CATS);
  const full = !isAdmin && cats.length >= MAX_GUEST_CATS;
  const premium = Boolean(user?.premium);
  const planName = isAdmin ? 'Plan Admin' : premium ? 'Plan Premium' : 'Plan gratuito';
  const unlimited = isAdmin || premium;

  return (
    <div className="screen-root">
      {/* 2. credencial */}
      <section className="credential-panel">
        <div className="credential-head">
          <div className="credential-avatar">
            <Avatar name={user?.username ?? 'Invitado'} size={64} />
          </div>
          <div className="credential-meta">
            <div className="credential-name-row">
              <h1 className="credential-name">{user?.username ?? 'Invitado'}</h1>
              <span className="role-chip">
                {user ? (user.role === 'admin' ? 'Admin' : 'Member') : 'Invitado'}
              </span>
            </div>
            <p className="credential-email">{user?.email ?? 'Creando caos sin cuenta en este navegador'}</p>
            <p className="credential-since">
              {user?.date_joined
                ? `En kitchi desde ${new Date(user.date_joined).toLocaleDateString('es-CO', { day: 'numeric', month: 'short', year: 'numeric' })}`
                : 'Los invitados crean hasta 3 gatos en el navegador'}
            </p>
          </div>
        </div>

        {/* mini métricas (solo datos reales: gatos, publicados, días) */}
        <div className="metrics">
          <div className="metric">
            <span className="metric__num">{cats.length}</span>
            <span className="metric__label">Gatos</span>
          </div>
          <div className="metric">
            <span className="metric__num">{user ? publishedCount : '—'}</span>
            <span className="metric__label">Publicados</span>
          </div>
          <div className="metric">
            <span className="metric__num">{daysHere ?? '—'}</span>
            <span className="metric__label">Días aquí</span>
          </div>
        </div>
      </section>

      {/* 3. plan y capacidad */}
      <section className="plan-panel" aria-label="Plan y capacidad">
        <div className="plan-head">
          <div className="plan-identity">
            <span className="plan-icon" aria-hidden="true">
              {isAdmin ? <ShieldCheck size={16} strokeWidth={2.5} /> : <Crown size={16} strokeWidth={2.5} />}
            </span>
            <span>
              <span className="plan-title">{planName}</span>
              <span className="plan-sub">{isAdmin ? 'Cuenta administrativa · sin límites' : 'Almacenamiento de personajes'}</span>
            </span>
          </div>
          {isAdmin ? (
            <span className="plan-chip plan-chip--admin"><ShieldCheck size={13} strokeWidth={2.6} aria-hidden="true" /> Admin</span>
          ) : premium ? (
            <span className="plan-chip plan-chip--premium">Premium</span>
          ) : full ? (
            <span className="plan-chip plan-chip--full">Límite alcanzado</span>
          ) : (
            <span className="plan-chip">{count}/{MAX_GUEST_CATS} espacios</span>
          )}
        </div>

        {!unlimited && (
          <>
            <div className="plan-bar-row">
              <span>Gatos guardados</span>
              <span>{count} / {MAX_GUEST_CATS} espacios</span>
            </div>
            <div className="plan-bar" role="progressbar" aria-valuenow={count} aria-valuemin={0} aria-valuemax={MAX_GUEST_CATS} aria-label="Gatos guardados">
              <div className="plan-bar__fill" style={{ width: `${(count / MAX_GUEST_CATS) * 100}%`, background: full ? 'var(--coral)' : 'var(--panel)' }} />
            </div>
          </>
        )}

        <div className="plan-cta-row">
          {unlimited ? (
            <span className="plan-cta plan-cta--premium" aria-hidden="true">
              <Check size={16} strokeWidth={3} /> Espacios ilimitados
            </span>
          ) : user ? (
            <button type="button" className="plan-cta plan-cta--soon" disabled title="Muy pronto">
              <Sparkles size={16} strokeWidth={2.4} /> Desbloquear espacios ilimitados <span className="filter-soon">Pronto</span>
            </button>
          ) : (
            <button type="button" className="plan-cta" onClick={() => navigate('/auth/register')}>
              <UserRoundPlus size={17} strokeWidth={2.4} /> Crear cuenta para sincronizar
            </button>
          )}
        </div>
      </section>

      {/* 4. cuenta y accesos */}
      <section className="access-section" aria-label="Cuenta y accesos">
        <h2 className="access-title">Cuenta y accesos</h2>
        <div className="tiles">
          <button
            type="button"
            className="tile"
            disabled={!user}
            title={user ? 'Ver mi tarjeta pública' : 'Crea tu cuenta para ver tu perfil público'}
            onClick={() => user && navigate(`/publico/${encodeURIComponent(user.username)}`)}
          >
            <span className="tile__icon tile__icon--public" aria-hidden="true">
              <ExternalLink size={18} strokeWidth={2.3} />
            </span>
            <span className="tile__label">Perfil público</span>
          </button>
          <button
            type="button"
            className="tile"
            onClick={() => navigate('/settings')}
          >
            <span className="tile__icon tile__icon--settings" aria-hidden="true">
              <Settings size={18} strokeWidth={2.3} />
            </span>
            <span className="tile__label">Configuración</span>
          </button>
        </div>

        {user ? (
          <button type="button" className="logout-btn" onClick={() => void logout()}>
            <LogOut size={17} strokeWidth={2.5} /> Cerrar sesión
          </button>
        ) : (
          <div className="auth-inline">
            <button type="button" className="bevel-btn-coral btn-block" onClick={() => navigate('/auth/register')}>
              <Cat size={16} strokeWidth={2.4} aria-hidden="true" /> Registrarse
            </button>
            <button type="button" className="bevel-btn btn-block" onClick={() => navigate('/auth/login')}>
              Iniciar sesión
            </button>
          </div>
        )}
      </section>
    </div>
  );
}
