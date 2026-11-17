// Crear / Editar: editor del gato chibi con vista previa en vivo.
// Estructura basada en el mockup testui/index.html: título + badge de modo,
// lienzo ámbar con estrellas y controles flotantes, input con lápiz,
// carrusel de categorías y rejilla de opciones; guardar abajo.
import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Check, Dices, Eye, Layers, Palette, Pencil, RotateCcw, Scissors, Shirt, Sparkles, Undo2, type LucideIcon,
} from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import { CATALOG, defaultConfig, normalizeConfiguration, type CatConfiguration } from '../lib/catalog';
import CatSVG from '../components/CatSVG';

const CATEGORY_ICONS: Record<string, LucideIcon> = {
  fur: Palette, eyes: Eye, hair: Scissors, top: Shirt, bottom: Layers, accessory: Sparkles,
};

const CATEGORY_LABELS: Record<string, string> = {
  fur: 'Pelaje', eyes: 'Ojos', hair: 'Cabello', top: 'Superior', bottom: 'Inferior', accessory: 'Extras',
};

const MAX_HISTORY = 60;

export default function EditorScreen() {
  const { cats, saveCat, user, animationsEnabled } = useKitchi();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const editingId = searchParams.get('cat');
  const editingCat = useMemo(
    () => (editingId ? cats.find((c) => String(c.id) === String(editingId)) ?? null : null),
    [cats, editingId],
  );

  const [configuration, setConfiguration] = useState<CatConfiguration>(() =>
    editingCat ? normalizeConfiguration(editingCat.configuration) : defaultConfig(),
  );
  const [history, setHistory] = useState<CatConfiguration[]>([]);
  const [catId, setCatId] = useState<string | null>(editingCat ? String(editingCat.id) : null);
  const [name, setName] = useState(editingCat?.name ?? '');
  const [selectedCategory, setSelectedCategory] = useState(CATALOG[0].key);
  const [saving, setSaving] = useState(false);

  // si llega el gato a editar tarde (tras bootstrap), precargar una sola vez
  const [prefilled, setPrefilled] = useState(Boolean(editingCat));
  useEffect(() => {
    if (prefilled || !editingCat) return;
    setConfiguration(normalizeConfiguration(editingCat.configuration));
    setCatId(String(editingCat.id));
    setName(editingCat.name);
    setPrefilled(true);
  }, [editingCat, prefilled]);

  const activeOptions = CATALOG.find((c) => c.key === selectedCategory)?.options ?? [];

  const pushHistory = (cfg: CatConfiguration) => {
    setHistory((prev) => [...prev.slice(-(MAX_HISTORY - 1)), cfg]);
  };

  const selectOption = (category: string, code: string) => {
    if (configuration[category as keyof CatConfiguration] === code) return;
    pushHistory(configuration);
    setConfiguration({ ...configuration, [category]: code });
  };

  const undo = () => {
    setHistory((prev) => {
      if (prev.length === 0) return prev;
      const next = [...prev];
      setConfiguration(next.pop() as CatConfiguration);
      return next;
    });
  };

  const reset = () => {
    pushHistory(configuration);
    setConfiguration(defaultConfig());
  };

  const randomize = () => {
    pushHistory(configuration);
    const next: Record<string, unknown> = { schema_version: 1 };
    for (const cat of CATALOG) {
      next[cat.key] = cat.options[Math.floor(Math.random() * cat.options.length)].code;
    }
    setConfiguration(next as unknown as CatConfiguration);
  };

  const handleSave = async () => {
    const clean = name.trim();
    if (!clean) {
      return;
    }
    setSaving(true);
    const saved = await saveCat(clean, configuration, catId);
    setSaving(false);
    if (saved) {
      setCatId(String(saved.id));
      if (editingId) navigate('/mis-gatos');
    }
  };

  const nameInvalid = name.trim().length === 0;

  return (
    <div className="screen-root screen-root--tight">
      {/* 1. fila de título + badge de modo */}
      <div className="editor-head">
        <h1 className="editor-title">
          {editingId ? 'Editar gato' : 'Crear gato'}
        </h1>
        <span className="mode-badge">
          {user ? 'En tu cuenta' : 'Modo invitado'}
        </span>
      </div>

      {/* 2. lienzo de previsualización con controles flotantes */}
      <section className="canvas-stage" aria-label="Vista previa del gato">
        <div className="canvas-stage__stars" aria-hidden="true" />

        {/* deshacer / reiniciar */}
        <div className="canvas-stage__tools">
          <button
            type="button"
            className="canvas-btn"
            onClick={undo}
            disabled={history.length === 0}
            title="Deshacer"
            aria-label="Deshacer"
          >
            <Undo2 size={17} strokeWidth={2.4} />
          </button>
          <button type="button" className="canvas-btn" onClick={reset} title="Reiniciar" aria-label="Reiniciar">
            <RotateCcw size={17} strokeWidth={2.4} />
          </button>
        </div>

        {/* aleatorio */}
        <button
          type="button"
          className="canvas-btn-amber canvas-stage__random"
          onClick={randomize}
          title="Combinación aleatoria"
        >
          <Dices size={16} strokeWidth={2.4} /> Aleatorio
        </button>

        <motion.div
          animate={animationsEnabled ? { y: [0, -7, 0] } : undefined}
          transition={{ duration: 2.6, repeat: Infinity, ease: 'easeInOut' }}
          className="canvas-stage__cat"
        >
          <CatSVG configuration={configuration} size={148} />
        </motion.div>
      </section>

      {/* 3. nombre con lápiz */}
      <label className="name-field">
        <span className="sr-only">Nombre del gato</span>
        <input
          className="name-field__input"
          placeholder="Nombre de tu gato..."
          value={name}
          maxLength={40}
          onChange={(e) => setName(e.target.value)}
          aria-label="Nombre del gato"
        />
        <span className="name-field__icon">
          <Pencil size={17} strokeWidth={2.2} />
        </span>
      </label>

      {/* 4. carrusel de categorías */}
      <div className="cat-carousel no-scrollbar" role="tablist" aria-label="Categorías">
        {CATALOG.map((cat) => {
          const Icon = CATEGORY_ICONS[cat.key];
          const active = cat.key === selectedCategory;
          return (
            <button
              key={cat.key}
              type="button"
              role="tab"
              aria-selected={active}
              className="cat-chip"
              data-active={active}
              onClick={() => setSelectedCategory(cat.key)}
            >
              <Icon size={20} strokeWidth={2.2} aria-hidden="true" />
              <span className="cat-chip__label">{CATEGORY_LABELS[cat.key]}</span>
            </button>
          );
        })}
      </div>

      {/* 5. opciones de la categoría */}
      <div className="options-grid" role="listbox" aria-label={`Opciones de ${selectedCategory}`}>
        {activeOptions.map((opt) => {
          const selected = configuration[selectedCategory as keyof CatConfiguration] === opt.code;
          return (
            <button
              key={opt.code}
              type="button"
              role="option"
              aria-selected={selected}
              className="option-card"
              data-selected={selected}
              onClick={() => selectOption(selectedCategory, opt.code)}
            >
              <span className="option-card__swatch" style={{ background: opt.swatch }} aria-hidden="true" />
              <span className="option-card__name">{opt.name}</span>
              {selected && (
                <span className="option-card__check" aria-hidden="true">
                  <Check size={11} strokeWidth={4} />
                </span>
              )}
            </button>
          );
        })}
      </div>

      {/* 6. botón principal */}
      <button
        type="button"
        className="save-btn"
        disabled={nameInvalid || saving}
        onClick={() => void handleSave()}
      >
        <Check size={22} strokeWidth={2.8} aria-hidden="true" />
        {saving ? 'Guardando…' : catId ? 'Guardar cambios' : 'Guardar gato'}
      </button>
    </div>
  );
}
