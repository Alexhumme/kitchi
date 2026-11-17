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
    <div className="screen-root">
      <SectionTitle title="Stickers IA" subtitle="De tu gato a un paquete compartible" />

      {/* el paquete */}
      <section className="stickers-panel">
        <h2 className="stickers-eyebrow">El paquete</h2>
        <p className="stickers-sub">Seis stickers PNG con fondo transparente</p>
        <div className="stickers-poses">
          {poses.map((pose) => (
            <span key={pose.code} className="bevel-chip">{pose.name}</span>
          ))}
        </div>
        <p className="stickers-meta">
          {poses.length} poses cargadas desde /api/poses/.
          {!apiOnline && ' (empaquetadas para el modo local)'}
        </p>
        <p className="stickers-body">
          El motor compondrá tu gato en las seis poses y podrás descargar cada PNG o el
          paquete completo. Mientras no existan los assets se usará el mismo placeholder
          de color del editor.
        </p>
      </section>

      {/* estado del motor */}
      <section className="stickers-panel">
        <div className="stickers-engine">
          <WandSparkles size={20} strokeWidth={2.3} className="stickers-engine-icon" aria-hidden="true" />
          <h2 className="stickers-engine-title">Generación pendiente (semana 3)</h2>
          <span className="badge badge--pink">P13–P16</span>
        </div>
        <p className="stickers-body">
          El motor gráfico (Pillow), el seguimiento de trabajos y la integración de IA aún no
          están implementados. Aquí verás el progreso real: pendiente, en proceso, completado
          o fallido.
        </p>
        <p className="stickers-warn">
          Nada se genera todavía: faltan /api/sticker-packs/ y /api/ai-jobs/ en el backend.
          Esta pantalla no simula resultados.
        </p>
      </section>

      {/* acción */}
      <section className="stickers-action">
        {cats.length === 0 ? (
          <EmptyState
            icon={<Cat size={34} strokeWidth={2.1} />}
            title="Primero crea un gato"
            body="Guarda un gato en el editor y podrás generar su paquete de stickers."
          />
        ) : (
          <label className="field-shell">
            <span className="field-label">Gato de partida</span>
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
        <button type="button" className="bevel-btn-coral btn-block stickers-generate" disabled>
          <WandSparkles size={19} strokeWidth={2.4} /> Generar 6 stickers
        </button>
        <p className="stickers-action__hint">
          {cats.length === 0 ? 'Guarda un gato en el editor para poder generar su paquete.' : 'Disponible cuando exista el motor de generación.'}
        </p>
      </section>
    </div>
  );
}
