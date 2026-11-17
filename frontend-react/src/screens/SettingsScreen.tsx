// Configuración de la app: acerca de, efectos, API y datos locales.
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ChevronLeft, Cat, CloudOff, Globe, RefreshCw, Sparkles, Trash, Vibrate, Volume2, type LucideIcon } from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import { pop, haptic } from '../lib/fx';
import { ConfirmDialog, SectionTitle, Toggle } from '../components/ui';

const APP_VERSION = '0.4.0';

const TECH_CHIPS = [
  { label: 'React', className: 'tech-chip tech-chip--react' },
  { label: 'Django REST', className: 'tech-chip tech-chip--django' },
  { label: 'MySQL', className: 'tech-chip tech-chip--mysql' },
  { label: 'Fredoka', className: 'tech-chip tech-chip--fredoka' },
];

function ToggleRow({ icon: Icon, iconClass, title, caption, checked, onChange }: {
  icon: LucideIcon;
  iconClass: string;
  title: string;
  caption: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <div className="toggle-row">
      <span aria-hidden="true" className={`toggle-row__icon ${iconClass}`}><Icon size={21} strokeWidth={2.2} /></span>
      <div className="toggle-row__text">
        <p className="toggle-row__title">{title}</p>
        <p className="toggle-row__caption">{caption}</p>
      </div>
      <Toggle checked={checked} onChange={onChange} label={title} />
    </div>
  );
}

export default function SettingsScreen() {
  const navigate = useNavigate();
  const {
    soundEnabled, animationsEnabled, hapticsEnabled,
    setSoundEnabled, setAnimationsEnabled, setHapticsEnabled,
    apiOnline, apiError, catalogSource, refreshAll, user, clearGuestCats, cats,
  } = useKitchi();
  const [confirmClear, setConfirmClear] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const toggleWithFx = (setter: (v: boolean) => void) => (v: boolean) => {
    setter(v);
    if (v) {
      pop('tap');
      haptic(12);
    }
  };

  const doRefresh = async () => {
    setRefreshing(true);
    await refreshAll();
    setRefreshing(false);
    pop('success');
  };

  return (
    <div className="screen-root">
      <header className="back-header">
        <button type="button" className="back-header__btn" onClick={() => navigate(-1)} aria-label="Volver">
          <ChevronLeft size={22} strokeWidth={2.4} />
        </button>
        <SectionTitle title="Configuración" />
        <span className="version-chip">v{APP_VERSION}</span>
      </header>

      {/* acerca de */}
      <section className="settings-about">
        <Cat size={48} strokeWidth={2} className="settings-brand" aria-hidden="true" />
        <h1 className="settings-title">kitchi.studio</h1>
        <p className="settings-tagline">Caos adorable, a tu manera</p>
        <p className="settings-blurb">
          Compón un gato chibi pieza a pieza, guárdalo en tu cuenta o en este navegador,
          publícalo en el hub y prepárate para el paquete de seis stickers.
        </p>
        <div className="settings-tech">
          {TECH_CHIPS.map((chip) => (
            <span key={chip.label} className={chip.className}>{chip.label}</span>
          ))}
        </div>
      </section>

      {/* así funciona */}
      <section className="settings-section">
        <SectionTitle title="Así funciona" subtitle="Tres pasos, cero talento requerido" />
        <ol className="settings-steps">
          {[
            ['1', 'Elige tus piezas', 'Seis categorías, tres opciones cada una: pelaje, ojos, cabello, ropa y extras.'],
            ['2', 'Combina sin miedo', 'Cambia lo que quieras en tiempo real y deshaz cuando el caos se pase de la raya.'],
            ['3', 'Guarda y comparte', 'Hasta 3 gatos por cuenta o en este navegador; publica en el hub.'],
          ].map(([n, t, d]) => (
            <li key={n} className="settings-steps__item">
              <span className="settings-steps__num">{n}</span>
              <span>
                <span className="settings-steps__title">{t}</span>
                <br />
                <span className="settings-steps__desc">{d}</span>
              </span>
            </li>
          ))}
        </ol>
      </section>

      {/* efectos */}
      <section className="settings-section">
        <SectionTitle title="Efectos" />
        <div className="toggle-rows">
          <ToggleRow icon={Volume2} iconClass="toggle-row__icon--mint" title="Sonido" caption="Rebotes y confirmaciones sintetizados con Web Audio." checked={soundEnabled} onChange={toggleWithFx(setSoundEnabled)} />
          <ToggleRow icon={Sparkles} iconClass="toggle-row__icon--lavender" title="Animaciones" caption="Rebote al tocar controles y fundidos al cambiar de sección." checked={animationsEnabled} onChange={toggleWithFx(setAnimationsEnabled)} />
          <ToggleRow icon={Vibrate} iconClass="toggle-row__icon--honey" title="Vibración táctil (móvil)" caption="Impulso breve al tocar botones y navegar. En escritorio no hace nada." checked={hapticsEnabled} onChange={toggleWithFx(setHapticsEnabled)} />
        </div>
        <button type="button" className="bevel-btn btn-xs settings-test-sound" onClick={() => pop('success')}>
          Probar sonido
        </button>
      </section>

      {/* datos */}
      <section className="settings-section">
        <SectionTitle title="Datos" />
        <div className="settings-data-row">
          <span className={`badge badge--${apiOnline ? 'ok' : 'error'}`}>
            {apiOnline
              ? <><Globe size={13} strokeWidth={2.6} aria-hidden="true" /> API en línea</>
              : <><CloudOff size={13} strokeWidth={2.6} aria-hidden="true" /> API sin conexión</>}
          </span>
          <span className="bevel-chip">Catálogo: {catalogSource === 'api' ? 'servidor' : 'empaquetado'}</span>
          {!user && <span className="bevel-chip">{cats.length} gato(s) en este navegador</span>}
        </div>
        {apiError && <p className="settings-error">{apiError}</p>}
        <div className="settings-actions">
          <button type="button" className="bevel-btn-yellow btn-xs" onClick={() => void doRefresh()} disabled={refreshing}>
            <RefreshCw size={15} strokeWidth={2.5} aria-hidden="true" /> {refreshing ? 'Actualizando…' : 'Actualizar datos'}
          </button>
          {!user && (
            <button type="button" className="bevel-btn btn-xs settings-danger" onClick={() => setConfirmClear(true)}>
              <Trash size={15} strokeWidth={2.5} aria-hidden="true" /> Vaciar datos locales
            </button>
          )}
        </div>
      </section>

      <p className="settings-footer">
        Fuente <a href="https://fonts.google.com/specimen/Fredoka" target="_blank" rel="noreferrer">Fredoka</a> (OFL) · Gato dibujado pieza a pieza · v{APP_VERSION}
      </p>

      <ConfirmDialog
        open={confirmClear}
        title="¿Vaciar los datos locales?"
        body="Se eliminarán todos los gatos guardados en este navegador. No se puede deshacer."
        confirmLabel="Vaciar todo"
        danger
        onConfirm={() => { clearGuestCats(); setConfirmClear(false); }}
        onCancel={() => setConfirmClear(false)}
      />
    </div>
  );
}
