// Armazón de Kitchi Studio: toolbar miel, contenido y barra inferior oscura.
import { BrowserRouter, Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { Cat, CirclePlus, CircleUserRound, Compass, PawPrint, Settings, Sticker, UserRound } from 'lucide-react';
import { KitchiProvider, useKitchi } from './state/AppContext';
import { ToastViewport } from './components/ui';
import Avatar from './components/Avatar';
import { pop, haptic } from './lib/fx';
import HubScreen from './screens/HubScreen';
import EditorScreen from './screens/EditorScreen';
import MyCatsScreen from './screens/MyCatsScreen';
import StickersScreen from './screens/StickersScreen';
import ProfileScreen from './screens/ProfileScreen';
import SettingsScreen from './screens/SettingsScreen';
import AuthScreen from './screens/AuthScreen';
import PublicProfileScreen from './screens/PublicProfileScreen';

const TABS = [
  { to: '/', label: 'Navegar', icon: Compass },
  { to: '/mis-gatos', label: 'Mis gatos', icon: PawPrint },
  { to: '/crear', label: 'Crear', icon: CirclePlus },
  { to: '/stickers', label: 'Stickers IA', icon: Sticker },
  { to: '/perfil', label: 'Perfil', icon: CircleUserRound },
];

function TabBar() {
  const location = useLocation();
  const navigate = useNavigate();
  const activeIndex = TABS.findIndex((tab) =>
    tab.to === '/' ? location.pathname === '/' : location.pathname.startsWith(tab.to),
  );
  return (
    <nav className="bottombar" aria-label="Secciones principales">
      <div className="bottombar__tabs">
        {TABS.map((tab, i) => {
          const active = i === activeIndex;
          return (
            <button
              key={tab.to}
              type="button"
              className="bottombar__tab"
              data-active={active}
              aria-current={active ? 'page' : undefined}
              onClick={() => {
                pop('nav');
                haptic(8);
                navigate(tab.to);
              }}
            >
              {active && (
                <motion.span
                  layoutId="tab-pill"
                  className="tab-indicator"
                  style={{ zIndex: 0 }}
                  transition={{ type: 'spring', stiffness: 520, damping: 38 }}
                />
              )}
              <span className="tab-icon" aria-hidden="true">
                <tab.icon size={24} strokeWidth={2.4} />
              </span>
              <span className="tab-label">{tab.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}

function Toolbar() {
  const navigate = useNavigate();
  const { user } = useKitchi();
  return (
    <header className="toolbar">
      <div className="toolbar__row">
        <button type="button" className="toolbar__brand" onClick={() => navigate('/')} aria-label="kitchi.studio, ir a Navegar">
          <span className="toolbar__icon" aria-hidden="true"><PawPrint size={20} strokeWidth={2.6} color="#fff" /></span>
          <span className="toolbar__brand-name">kitchi.studio</span>
        </button>
        <div className="toolbar__spacer" />
        <button type="button" className="toolbar__action" onClick={() => navigate('/settings')} aria-label="Configuración de la app">
          <Settings size={20} strokeWidth={2.4} />
        </button>
        <button type="button" className="toolbar__identity" onClick={() => navigate(user ? '/perfil' : '/auth/login')} aria-label={user ? 'Ir a tu perfil' : 'Entrar o crear cuenta'}>
          {user ? <Avatar name={user.username} size={26} /> : <span className="toolbar__identity-icon" aria-hidden="true"><UserRound size={15} strokeWidth={2.6} /></span>}
          <span className="toolbar__identity-name">{user?.username ?? 'Invitado'}</span>
        </button>
      </div>
      <div className="separator" aria-hidden="true" />
    </header>
  );
}

function Splash() {
  return (
    <div className="app-bg splash">
      <motion.div
        animate={{ scale: [1, 1.12, 1], rotate: [0, -6, 6, 0] }}
        transition={{ duration: 1.6, repeat: Infinity, ease: 'easeInOut' }}
        className="splash__icon"
        aria-hidden="true"
      >
        <Cat size={52} strokeWidth={2.2} />
      </motion.div>
      <p className="splash__brand">kitchi.studio</p>
      <p className="splash__hint">Abriendo el estudio…</p>
    </div>
  );
}

function Shell() {
  const location = useLocation();
  const { bootstrapping, storageNotice, animationsEnabled } = useKitchi();

  if (bootstrapping) {
    return (
      <div className="app-shell">
        <div className="phone">
          <Splash />
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <div className="phone app-bg">
        <Toolbar />
        <main className="shell-main">
          {storageNotice && (
            <p className="offline-banner" role="status">
              {storageNotice}
            </p>
          )}
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={location.pathname}
              className="page-motion"
              initial={animationsEnabled ? { opacity: 0, x: 34 } : false}
              animate={{ opacity: 1, x: 0 }}
              exit={animationsEnabled ? { opacity: 0, x: -22 } : undefined}
              transition={{ duration: 0.22, ease: 'easeOut' }}
            >
              <Routes location={location}>
                <Route path="/" element={<HubScreen />} />
                <Route path="/mis-gatos" element={<MyCatsScreen />} />
                <Route path="/crear" element={<EditorScreen />} />
                <Route path="/stickers" element={<StickersScreen />} />
                <Route path="/perfil" element={<ProfileScreen />} />
                <Route path="/settings" element={<SettingsScreen />} />
                <Route path="/auth/:mode" element={<AuthScreen />} />
                <Route path="/publico/:username" element={<PublicProfileScreen />} />
                <Route path="*" element={<HubScreen />} />
              </Routes>
            </motion.div>
          </AnimatePresence>
        </main>
        <ToastViewport />
        <TabBar />
      </div>
    </div>
  );
}

export default function App() {
  return (
    <KitchiProvider>
      <BrowserRouter>
        <Shell />
      </BrowserRouter>
    </KitchiProvider>
  );
}
