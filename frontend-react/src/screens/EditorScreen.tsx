// Crear / Editar: editor del gato chibi con vista previa en vivo.
import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useKitchi } from '../state/AppContext';
import { CATALOG, defaultConfig, normalizeConfiguration, type CatConfiguration } from '../lib/catalog';
import CatSVG from '../components/CatSVG';
import { SectionTitle } from '../components/ui';
import { Dices, Check, Eye, Layers, Palette, RotateCcw, Scissors, Shirt, Sparkles, Undo2, type LucideIcon } from 'lucide-react';

const CATEGORY_ICONS: Record<string, LucideIcon> = {
  fur: Palette, eyes: Eye, hair: Scissors, top: Shirt, bottom: Layers, accessory: Sparkles,
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
  const [dirty, setDirty] = useState(false);
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
    setDirty(true);
  };

  const undo = () => {
    setHistory((prev) => {
      if (prev.length === 0) return prev;
      const next = [...prev];
      setConfiguration(next.pop() as CatConfiguration);
      setDirty(true);
      return next;
    });
  };

  const reset = () => {
    pushHistory(configuration);
    setConfiguration(defaultConfig());
    setDirty(true);
  };

  const randomize = () => {
    pushHistory(configuration);
    const next: Record<string, unknown> = { schema_version: 1 };
    for (const cat of CATALOG) {
      next[cat.key] = cat.options[Math.floor(Math.random() * cat.options.length)].code;
    }
    setConfiguration(next as unknown as CatConfiguration);
    setDirty(true);
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
      setDirty(false);
      if (editingId) navigate('/mis-gatos');
    }
  };

  const nameInvalid = name.trim().length === 0;

  return (
    <div className="app-scroll flex h-full flex-col gap-3 overflow-y-auto pr-1">
      <div className="flex items-start justify-between gap-3">
        <SectionTitle
          title={editingId ? 'Editar gato' : 'Crear gato'}
          subtitle={user ? 'Se guarda en tu cuenta' : 'Se guarda en este navegador (modo invitado)'}
        />
        {dirty && <span className="badge badge--warn shrink-0">Sin guardar</span>}
      </div>

      {/* vista previa */}
      <div className="bevel-panel relative shrink-0 overflow-hidden !rounded-[var(--radio-grande)]">
        <div className="preview-stage">
          <div className="preview-stage__pattern" aria-hidden="true" />
          <motion.div
            animate={animationsEnabled ? { y: [0, -8, 0] } : undefined}
            transition={{ duration: 2.6, repeat: Infinity, ease: 'easeInOut' }}
            className="relative"
          >
            <CatSVG configuration={configuration} size={132} />
          </motion.div>
        </div>
      </div>

      {/* nombre */}
      <label className="field-shell shrink-0 !rounded-[var(--radio-pastilla)] px-4 py-1">
        <span className="sr-only">Nombre del gato</span>
        <input
          className="field-shell__input"
          placeholder="Nombre del gato…"
          value={name}
          maxLength={40}
          onChange={(e) => setName(e.target.value)}
          aria-label="Nombre del gato"
        />
      </label>

      {/* selector de categoría */}
      <div className="grid shrink-0 grid-cols-6 gap-1.5">
        {CATALOG.map((cat) => {
          const active = cat.key === selectedCategory;
          return (
            <button
              key={cat.key}
              type="button"
              className="cat-tab"
              data-active={active}
              onClick={() => setSelectedCategory(cat.key)}
              aria-pressed={active}
            >
              <span aria-hidden="true" className="cat-tab__icon">
                {(() => { const Icon = CATEGORY_ICONS[cat.key]; return <Icon size={19} strokeWidth={2.3} />; })()}
              </span>
              <span className="cat-tab__label">{cat.label}</span>
            </button>
          );
        })}
      </div>

      {/* opciones */}
      <div className="grid shrink-0 grid-cols-3 gap-2" role="listbox" aria-label={`Opciones de ${selectedCategory}`}>
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

      {/* historial / aleatorio */}
      <div className="flex shrink-0 items-center justify-between gap-2">
        <div className="flex gap-2">
          <button type="button" className="bevel-btn flex items-center gap-1.5 px-3 py-2 text-xs font-extrabold disabled:opacity-40" onClick={undo} disabled={history.length === 0}>
            <Undo2 size={15} strokeWidth={2.6} /> Deshacer
          </button>
          <button type="button" className="bevel-btn flex items-center gap-1.5 px-3 py-2 text-xs font-extrabold" onClick={reset}>
            <RotateCcw size={15} strokeWidth={2.6} /> Reiniciar
          </button>
        </div>
        <button type="button" className="bevel-btn-yellow flex items-center gap-1.5 px-4 py-2 text-xs" onClick={randomize}>
          <Dices size={16} strokeWidth={2.4} /> Aleatorio
        </button>
      </div>

      {/* guardar */}
      <button
        type="button"
        className="bevel-btn-coral mb-1 w-full shrink-0 py-3.5 text-base disabled:opacity-50"
        disabled={nameInvalid || saving}
        onClick={() => void handleSave()}
      >
        {saving ? 'Guardando…' : catId ? 'Guardar cambios' : 'Guardar gato'}
      </button>
    </div>
  );
}
