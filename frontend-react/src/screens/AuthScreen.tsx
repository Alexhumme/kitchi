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
    <div className="screen-root screen-root--center">
      <motion.div
        initial={{ scale: 0.6, opacity: 0, rotate: -8 }}
        animate={{ scale: 1, opacity: 1, rotate: 0 }}
        transition={{ type: 'spring', stiffness: 300, damping: 18 }}
        className="auth-hero"
        aria-hidden="true"
      >
        <Cat size={42} strokeWidth={2.2} />
      </motion.div>
      <SectionTitle
        title={isRegister ? 'Crear cuenta' : 'Iniciar sesión'}
      />

      <form onSubmit={(e) => void submit(e)} className="auth-form" noValidate>
        <label className="auth-field">
          <span className="field-label">Usuario</span>
          <input
            className="auth-field__input"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            autoComplete="username"
            required
            minLength={3}
            autoFocus
          />
        </label>
        {isRegister && (
          <label className="auth-field">
            <span className="field-label">Correo</span>
            <input
              className="auth-field__input"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
          </label>
        )}
        <label className="auth-field">
          <span className="field-label">Contraseña</span>
          <input
            className="auth-field__input auth-field__input--with-toggle"
            type={showPassword ? 'text' : 'password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            autoComplete={isRegister ? 'new-password' : 'current-password'}
            required
            minLength={8}
          />
          <button
            type="button"
            className="auth-field__toggle"
            onClick={() => setShowPassword((v) => !v)}
            aria-label={showPassword ? 'Ocultar contraseña' : 'Mostrar contraseña'}
          >
            {showPassword ? <EyeOff size={19} strokeWidth={2.3} /> : <Eye size={19} strokeWidth={2.3} />}
          </button>
        </label>

        {error && (
          <p role="alert" className="auth-error">
            {error}
          </p>
        )}

        <button type="submit" className="bevel-btn-coral btn-lg btn-block" disabled={submitting}>
          {submitting ? 'Un momento…' : isRegister ? 'Crear cuenta' : 'Entrar'}
        </button>
      </form>

      <div className="auth-foot">
        {isRegister ? (
          <p>¿Ya tienes cuenta?{' '}
            <button type="button" className="auth-link" onClick={() => navigate('/auth/login')}>
              Inicia sesión
            </button>
          </p>
        ) : (
          <p>¿Primera vez aquí?{' '}
            <button type="button" className="auth-link" onClick={() => navigate('/auth/register')}>
              Crea tu cuenta
            </button>
          </p>
        )}
        <button type="button" className="auth-link auth-link--subtle" onClick={() => navigate('/')}>
          Seguir como invitado →
        </button>
      </div>
    </div>
  );
}
