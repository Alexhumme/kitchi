// Stickers IA: flujo de seis poses. El motor (P13–P16) aún no existe;
// la pantalla muestra las poses reales de la API sin simular resultados.
import { useState } from 'react';
import { useKitchi } from '../state/AppContext';
import { EmptyState, SectionTitle } from '../components/ui';
import { Cat, WandSparkles } from 'lucide-react';

export default function StickersScreen() {
  const { cats, poses, apiOnline } = useKitchi();
  const [selectedCat, setSelectedCat] = useState('');

  return (
    <div className="app-scroll flex h-full flex-col gap-3 overflow-y-auto pr-1">
      <SectionTitle title="Stickers IA" subtitle="De tu gato a un paquete compartible" />

      {/* el paquete */}
      <section className="bevel-panel shrink-0 p-4">
        <h2 className="text-sm font-extrabold uppercase tracking-wide text-[var(--ink)]">El paquete</h2>
        <p className="mt-0.5 text-[0.78rem] font-semibold text-[var(--tinta-suave)]">Seis stickers PNG con fondo transparente</p>
        <div className="mt-3 flex flex-wrap gap-2">
          {poses.map((pose) => (
            <span key={pose.code} className="bevel-chip">{pose.name}</span>
          ))}
        </div>
        <p className="mt-2 text-[0.72rem] font-semibold text-[var(--tinta-suave)]">
          {poses.length} poses cargadas desde /api/poses/.
          {!apiOnline && ' (empaquetadas para el modo local)'}
        </p>
        <p className="mt-2 text-[0.85rem] font-medium leading-snug text-[var(--ink-soft)]">
          El motor compondrá tu gato en las seis poses y podrás descargar cada PNG o el
          paquete completo. Mientras no existan los assets se usará el mismo placeholder
          de color del editor.
        </p>
      </section>

      {/* estado del motor */}
      <section className="bevel-panel shrink-0 p-4">
        <div className="flex items-center gap-2">
          <WandSparkles size={20} strokeWidth={2.3} className="text-[var(--violeta)]" aria-hidden="true" />
          <h2 className="text-sm font-extrabold text-[var(--ink)]">Generación pendiente (semana 3)</h2>
          <span className="badge badge--pink">P13–P16</span>
        </div>
        <p className="mt-2 text-[0.85rem] font-medium leading-snug text-[var(--ink-soft)]">
          El motor gráfico (Pillow), el seguimiento de trabajos y la integración de IA aún no
          están implementados. Aquí verás el progreso real: pendiente, en proceso, completado
          o fallido.
        </p>
        <p className="mt-2 rounded-xl bg-[var(--panel-claro)] px-3 py-2 text-[0.78rem] font-semibold text-[var(--advertencia)]">
          Nada se genera todavía: faltan /api/sticker-packs/ y /api/ai-jobs/ en el backend.
          Esta pantalla no simula resultados.
        </p>
      </section>

      {/* acción */}
      <section className="flex shrink-0 flex-col gap-2 pb-1">
        {cats.length === 0 ? (
          <EmptyState
            icon={<Cat size={34} strokeWidth={2.1} />}
            title="Primero crea un gato"
            body="Guarda un gato en el editor y podrás generar su paquete de stickers."
          />
        ) : (
          <label className="field-shell !rounded-[var(--radio-medio)] px-4 py-1">
            <span className="text-[0.7rem] font-extrabold uppercase tracking-wide text-[var(--tinta-suave)]">Gato de partida</span>
            <select
              className="field-shell__input"
              value={selectedCat}
              onChange={(e) => setSelectedCat(e.target.value)}
            >
              <option value="">Elige un gato guardado…</option>
              {cats.map((cat) => (
                <option key={cat.id} value={String(cat.id)}>{cat.name}</option>
              ))}
            </select>
          </label>
        )}
        <button type="button" className="bevel-btn-coral flex w-full items-center justify-center gap-2 py-3.5 text-base opacity-60" disabled>
          <WandSparkles size={19} strokeWidth={2.4} /> Generar 6 stickers
        </button>
        <p className="text-center text-[0.72rem] font-semibold text-[var(--tinta-suave)]">
          {cats.length === 0 ? 'Guarda un gato en el editor para poder generar su paquete.' : 'Disponible cuando exista el motor de generación.'}
        </p>
      </section>
    </div>
  );
}
