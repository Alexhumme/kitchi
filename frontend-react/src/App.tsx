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
    <nav className="bottombar shrink-0" aria-label="Secciones principales">
      <div className="bottombar__rainbow" aria-hidden="true" />
      <div className="flex items-end justify-around px-1 pb-2 pt-1.5">
        {TABS.map((tab, i) => {
          const active = i === activeIndex;
          return (
            <button
              key={tab.to}
              type="button"
              className="bottombar__tab relative"
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
                  className="absolute inset-0 rounded-[var(--radio-pastilla)] bg-[var(--panel)]"
                  style={{ zIndex: 0 }}
                  transition={{ type: 'spring', stiffness: 520, damping: 38 }}
                />
              )}
              <span className="tab-icon tab-icon--svg relative" aria-hidden="true">
                <tab.icon size={24} strokeWidth={2.4} />
              </span>
              <span className="relative text-[0.62rem] font-extrabold leading-none">{tab.label}</span>
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
    <header className="toolbar shrink-0">
      <div className="flex items-center gap-2 px-4 pb-2 pt-3">
        <button type="button" className="toolbar__brand" onClick={() => navigate('/')} aria-label="kitchi.studio, ir a Navegar">
          <span className="toolbar__icon" aria-hidden="true"><PawPrint size={20} strokeWidth={2.6} color="#fff" /></span>
          <span className="text-[1.05rem] font-extrabold tracking-tight text-[var(--ink)]">kitchi.studio</span>
        </button>
        <div className="flex-1" />
        <button type="button" className="grid h-11 w-11 place-items-center rounded-full border-[3px] border-[var(--ink)] bg-[var(--superficie)] text-[var(--ink)] shadow-[0_3px_0_0_rgba(33,27,38,0.4)] transition-transform hover:-translate-y-0.5 active:translate-y-0.5" onClick={() => navigate('/settings')} aria-label="Configuración de la app">
          <Settings size={20} strokeWidth={2.4} />
        </button>
        <button type="button" className="flex items-center gap-1.5 rounded-full border-[3px] border-[var(--ink)] bg-[var(--crema-hondo)] py-1 pl-1 pr-3 shadow-[0_3px_0_0_rgba(33,27,38,0.4)] transition-transform hover:-translate-y-0.5 active:translate-y-0.5" onClick={() => navigate(user ? '/perfil' : '/auth/login')} aria-label={user ? 'Ir a tu perfil' : 'Entrar o crear cuenta'}>
          {user ? <Avatar name={user.username} size={26} /> : <span className="grid h-[26px] w-[26px] place-items-center rounded-full bg-[var(--lavanda)] text-[var(--ink)]" aria-hidden="true"><UserRound size={15} strokeWidth={2.6} /></span>}
          <span className="max-w-[72px] truncate text-[0.78rem] font-extrabold text-[var(--ink)]">{user?.username ?? 'Invitado'}</span>
        </button>
      </div>
      <div className="separator" aria-hidden="true" />
    </header>
  );
}

function Splash() {
  return (
    <div className="app-bg flex h-full flex-col items-center justify-center gap-4">
      <motion.div
        animate={{ scale: [1, 1.12, 1], rotate: [0, -6, 6, 0] }}
        transition={{ duration: 1.6, repeat: Infinity, ease: 'easeInOut' }}
        className="grid h-24 w-24 place-items-center rounded-[var(--radio-grande)] bg-[var(--coral)] text-white shadow-[inset_-6px_-7px_0_0_var(--coral-hondo),0_8px_0_0_rgba(33,27,38,0.35)]"
        aria-hidden="true"
      >
        <Cat size={52} strokeWidth={2.2} />
      </motion.div>
      <p className="text-sm font-extrabold uppercase tracking-widest text-[var(--ink)]">kitchi.studio</p>
      <p className="text-xs font-semibold text-[var(--tinta-suave)]">Abriendo el estudio…</p>
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
        <main className="relative flex-1 overflow-hidden px-3.5 pb-2 pt-3">
          {storageNotice && (
            <p className="mb-2 shrink-0 rounded-xl bg-[var(--panel-claro)] px-3 py-2 text-[0.72rem] font-semibold text-[var(--advertencia)]">
              {storageNotice}
            </p>
          )}
          <AnimatePresence mode="wait" initial={false}>
            <motion.div
              key={location.pathname}
              className="h-full"
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
