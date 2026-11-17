// Configuración de la app: acerca de, efectos, API y datos locales.
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useKitchi } from '../state/AppContext';
import { pop, haptic } from '../lib/fx';
import { ConfirmDialog, SectionTitle, Toggle } from '../components/ui';
import checkerSoft from '../assets/ui/patterns/checker_soft.png';
import { Cat, CloudOff, Globe, RefreshCw, Sparkles, Trash, Vibrate, Volume2, type LucideIcon } from 'lucide-react';

const APP_VERSION = '0.4.0';

function ToggleRow({ icon: Icon, title, caption, checked, onChange }: {
  icon: LucideIcon;
  title: string;
  caption: string;
  checked: boolean;
  onChange: (v: boolean) => void;
}) {
  return (
    <div className="flex items-center gap-3 py-1.5">
      <span aria-hidden="true" className="grid w-7 place-items-center text-[var(--ink)]"><Icon size={21} strokeWidth={2.2} /></span>
      <div className="min-w-0 flex-1">
        <p className="text-[0.88rem] font-bold leading-tight text-[var(--ink)]">{title}</p>
        <p className="text-[0.7rem] font-medium leading-snug text-[var(--tinta-suave)]">{caption}</p>
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
    <div className="app-scroll h-full overflow-y-auto pr-1">
      <header className="flex shrink-0 items-center gap-2 pt-1">
        <button type="button" className="grid h-10 w-10 place-items-center rounded-full text-[var(--ink)] hover:bg-black/5" onClick={() => navigate(-1)} aria-label="Volver">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.4" strokeLinecap="round" strokeLinejoin="round"><path d="M15 18l-6-6 6-6" /></svg>
        </button>
        <SectionTitle title="Configuración" subtitle="acerca de la app, sus efectos y datos" />
        <span className="ml-auto bevel-chip">v{APP_VERSION}</span>
      </header>

      {/* acerca de */}
      <section className="bevel-panel mt-3 shrink-0 !rounded-[var(--radio-grande)] p-5 text-center" style={{ backgroundImage: `url(${checkerSoft})`, backgroundSize: '120px' }}>
        <Cat size={48} strokeWidth={2} className="mx-auto text-[var(--ink)]" aria-hidden="true" />
        <h1 className="mt-1 text-2xl font-extrabold text-[var(--ink)]">kitchi.studio</h1>
        <p className="text-[0.85rem] font-bold text-[var(--tinta-suave)]">Caos adorable, a tu manera</p>
        <p className="mx-auto mt-2 max-w-[30ch] text-[0.82rem] font-medium leading-snug text-[var(--ink-soft)]">
          Compón un gato chibi pieza a pieza, guárdalo en tu cuenta o en este navegador,
          publícalo en el hub y prepárate para el paquete de seis stickers.
        </p>
        <div className="mt-3 flex flex-wrap justify-center gap-1.5">
          <span className="bevel-chip">React</span>
          <span className="bevel-chip">Django REST</span>
          <span className="bevel-chip">MySQL</span>
          <span className="bevel-chip">Fredoka</span>
        </div>
      </section>

      {/* así funciona */}
      <section className="bevel-panel mt-3 shrink-0 p-4">
        <SectionTitle title="Así funciona" subtitle="Tres pasos, cero talento requerido" />
        <ol className="mt-2 space-y-2">
          {[
            ['1', 'Elige tus piezas', 'Seis categorías, tres opciones cada una: pelaje, ojos, cabello, ropa y extras.'],
            ['2', 'Combina sin miedo', 'Cambia lo que quieras en tiempo real y deshaz cuando el caos se pase de la raya.'],
            ['3', 'Guarda y comparte', 'Hasta 3 gatos por cuenta o en este navegador; publica en el hub.'],
          ].map(([n, t, d]) => (
            <li key={n} className="flex items-start gap-3">
              <span className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-[var(--panel)] text-[0.8rem] font-extrabold text-[var(--ink)] shadow-[inset_-2px_-2px_0_0_var(--advertencia)]">{n}</span>
              <span>
                <span className="text-[0.85rem] font-extrabold text-[var(--ink)]">{t}</span>
                <br />
                <span className="text-[0.75rem] font-medium leading-snug text-[var(--ink-soft)]">{d}</span>
              </span>
            </li>
          ))}
        </ol>
      </section>

      {/* efectos */}
      <section className="bevel-panel mt-3 shrink-0 p-4">
        <SectionTitle title="Efectos" />
        <div className="mt-1.5 divide-y divide-[var(--crema-hondo)]">
          <ToggleRow icon={Volume2} title="Sonido" caption="Rebotes y confirmaciones sintetizados con Web Audio." checked={soundEnabled} onChange={toggleWithFx(setSoundEnabled)} />
          <ToggleRow icon={Sparkles} title="Animaciones" caption="Rebote al tocar controles y fundidos al cambiar de sección." checked={animationsEnabled} onChange={toggleWithFx(setAnimationsEnabled)} />
          <ToggleRow icon={Vibrate} title="Vibración táctil (móvil)" caption="Impulso breve al tocar botones y navegar. En escritorio no hace nada." checked={hapticsEnabled} onChange={toggleWithFx(setHapticsEnabled)} />
        </div>
        <button type="button" className="bevel-btn mt-2 px-4 py-2 text-xs font-extrabold" onClick={() => pop('success')}>
          Probar sonido
        </button>
      </section>

      {/* datos */}
      <section className="bevel-panel mt-3 shrink-0 p-4">
        <SectionTitle title="Datos" />
        <div className="mt-1.5 flex flex-wrap items-center gap-2 text-[0.78rem] font-semibold">
          <span className={`badge ${apiOnline ? 'badge--ok' : 'badge--error'} inline-flex items-center gap-1.5`}>
            {apiOnline ? <Globe size={13} strokeWidth={2.6} aria-hidden="true" /> : <CloudOff size={13} strokeWidth={2.6} aria-hidden="true" />}
            {apiOnline ? 'API en línea' : 'API sin conexión'}
          </span>
          <span className="bevel-chip">Catálogo: {catalogSource === 'api' ? 'servidor' : 'empaquetado'}</span>
          {!user && <span className="bevel-chip">{cats.length} gato(s) en este navegador</span>}
        </div>
        {apiError && <p className="mt-2 text-[0.75rem] font-semibold text-[var(--error)]">{apiError}</p>}
        <div className="mt-3 flex flex-wrap gap-2">
          <button type="button" className="bevel-btn flex items-center gap-1.5 px-4 py-2 text-xs font-extrabold disabled:opacity-50" onClick={() => void doRefresh()} disabled={refreshing}>
            <RefreshCw size={15} strokeWidth={2.5} aria-hidden="true" /> {refreshing ? 'Actualizando…' : 'Actualizar datos'}
          </button>
          {!user && (
            <button type="button" className="bevel-btn flex items-center gap-1.5 px-4 py-2 text-xs font-extrabold text-[var(--error)]" onClick={() => setConfirmClear(true)}>
              <Trash size={15} strokeWidth={2.5} aria-hidden="true" /> Vaciar datos locales
            </button>
          )}
        </div>
      </section>

      <p className="shrink-0 py-3 text-center text-[0.68rem] font-semibold text-[var(--tinta-suave)]">
        Fuente <a className="underline underline-offset-2" href="https://fonts.google.com/specimen/Fredoka" target="_blank" rel="noreferrer">Fredoka</a> (OFL) · Gato dibujado pieza a pieza · v{APP_VERSION}
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
