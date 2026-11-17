// Acceso: registro e inicio de sesión contra /api/auth/.
import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Cat, Eye, EyeOff } from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import { SectionTitle } from '../components/ui';

export default function AuthScreen() {
  const { mode } = useParams<{ mode: string }>();
  const isRegister = mode === 'register';
  const navigate = useNavigate();
  const { login, user } = useKitchi();

  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (user) navigate('/mis-gatos', { replace: true });
  }, [user, navigate]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSubmitting(true);
    const failure = await login(isRegister ? 'register' : 'login', username.trim(), email.trim(), password);
    setSubmitting(false);
    if (failure) {
      setError(failure);
      return;
    }
    navigate('/mis-gatos', { replace: true });
  };

  return (
    <div className="app-scroll flex h-full flex-col items-center justify-center gap-4 overflow-y-auto py-4">
      <motion.div
        initial={{ scale: 0.6, opacity: 0, rotate: -8 }}
        animate={{ scale: 1, opacity: 1, rotate: 0 }}
        transition={{ type: 'spring', stiffness: 300, damping: 18 }}
        className="grid h-20 w-20 place-items-center rounded-[var(--radio-grande)] bg-[var(--coral)] text-[#fff] shadow-[inset_-5px_-6px_0_0_var(--coral-hondo)]"
        aria-hidden="true"
      >
        <Cat size={42} strokeWidth={2.2} />
      </motion.div>
      <SectionTitle
        title={isRegister ? 'Crear cuenta' : 'Iniciar sesión'}
        subtitle={isRegister ? 'Sincroniza tus gatos y publica en el hub' : 'Tu cuenta guarda tus gatos en la nube'}
      />

      <form onSubmit={(e) => void submit(e)} className="bevel-panel w-full max-w-xs space-y-3 p-5" noValidate>
        <label className="field-shell block !rounded-[var(--radio-medio)] px-4 py-1">
          <span className="text-[0.68rem] font-extrabold uppercase tracking-wide text-[var(--tinta-suave)]">Usuario</span>
          <input
            className="field-shell__input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
            minLength={3}
            autoFocus
          />
        </label>
        {isRegister && (
          <label className="field-shell block !rounded-[var(--radio-medio)] px-4 py-1">
            <span className="text-[0.68rem] font-extrabold uppercase tracking-wide text-[var(--tinta-suave)]">Correo</span>
            <input
              className="field-shell__input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
          </label>
        )}
        <label className="field-shell relative block !rounded-[var(--radio-medio)] px-4 py-1">
          <span className="text-[0.68rem] font-extrabold uppercase tracking-wide text-[var(--tinta-suave)]">Contraseña</span>
          <input
            className="field-shell__input pr-10"
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete={isRegister ? 'new-password' : 'current-password'}
            required
            minLength={8}
          />
          <button
            type="button"
            className="absolute right-3 top-1/2 -translate-y-1/2 text-[var(--tinta-suave)] hover:text-[var(--ink)]"
            onClick={() => setShowPassword((v) => !v)}
            aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
          >
            {showPassword ? <EyeOff size={19} strokeWidth={2.3} /> : <Eye size={19} strokeWidth={2.3} />}
          </button>
        </label>

        {error && (
          <p role="alert" className="rounded-xl bg-[var(--coral-suave)] px-3 py-2 text-[0.8rem] font-semibold text-[var(--error)]">
            {error}
          </p>
        )}

        <button type="submit" className="bevel-btn-coral w-full py-3 text-base disabled:opacity-60" disabled={submitting}>
          {submitting ? 'Un momento…' : isRegister ? 'Crear cuenta' : 'Entrar'}
        </button>
      </form>

      <div className="flex flex-col items-center gap-1.5 text-[0.82rem] font-semibold text-[var(--tinta-suave)]">
        {isRegister ? (
          <p>¿Ya tienes cuenta?{' '}
            <button type="button" className="font-extrabold text-[var(--coral)] underline underline-offset-2" onClick={() => navigate('/auth/login')}>
              Inicia sesión
            </button>
          </p>
        ) : (
          <p>¿Primera vez aquí?{' '}
            <button type="button" className="font-extrabold text-[var(--coral)] underline underline-offset-2" onClick={() => navigate('/auth/register')}>
              Crea tu cuenta
            </button>
          </p>
        )}
        <button type="button" className="text-[0.78rem] underline underline-offset-2 opacity-80 hover:opacity-100" onClick={() => navigate('/')}>
          Seguir como invitado →
        </button>
      </div>
    </div>
  );
}
