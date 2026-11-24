// Crear / Editar: editor del gato chibi con vista previa en vivo.
import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  Check, Dices, Eye, Layers, Palette, Pencil, RotateCcw, Scissors, Shirt, Sparkles, Undo2, X, type LucideIcon,
} from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import {
  CATALOG,
  COLOR_KEYS,
  CONFIG_CATEGORY_KEYS,
  categoryBlock,
  defaultConfig,
  editorOptions,
  normalizeConfiguration,
  type CatConfiguration,
  type CategoryKey,
  type ConfigCategoryKey,
} from '../lib/catalog';
import { ACCESSORIES, accessoryByCode } from '../lib/characters';
import { colorAtHue, hueOf } from '../lib/color';
import CatSVG from '../components/CatSVG';

const CATEGORY_ICONS: Record<CategoryKey, LucideIcon> = {
  fur: Palette, eyes: Eye, hair: Scissors, top: Shirt, bottom: Layers, accessory: Sparkles,
};

const CATEGORY_LABELS: Record<CategoryKey, string> = {
  fur: 'Pelaje', eyes: 'Ojos', hair: 'Cabello', top: 'Superior', bottom: 'Inferior', accessory: 'Extras',
};

const MAX_HISTORY = 60;
const COLOR_CATEGORIES: ConfigCategoryKey[] = ['hair', 'top', 'bottom'];

type SingleCategory = Exclude<CategoryKey, 'accessory'>;

function keepColors(key: ConfigCategoryKey, code: string, current: CatConfiguration): CatConfiguration[ConfigCategoryKey] {
  const next = categoryBlock(key, code);
  const previous = current[key];
  for (const slot of COLOR_KEYS[key]) {
    if (previous[slot]) next[slot] = previous[slot];
  }
  return next;
}

function previewFor(
  configuration: CatConfiguration,
  category: CategoryKey,
  code: string,
): CatConfiguration {
  if (category === 'accessory') {
    const current = configuration.accessories.find((entry) => entry.code === code);
    return { ...configuration, accessories: [{ code, color: current?.color }] };
  }
  const key = category as ConfigCategoryKey;
  return { ...configuration, [key]: keepColors(key, code, configuration) };
}

export default function EditorScreen() {
  const { cats, saveCat, user, animationsEnabled } = useKitchi();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const editingId = searchParams.get('cat');
  const editingCat = useMemo(
    () => (editingId ? cats.find((cat) => String(cat.id) === String(editingId)) ?? null : null),
    [cats, editingId],
  );

  const [configuration, setConfiguration] = useState<CatConfiguration>(() =>
    editingCat ? normalizeConfiguration(editingCat.configuration) : defaultConfig(),
  );
  const [history, setHistory] = useState<CatConfiguration[]>([]);
  const [catId, setCatId] = useState<string | null>(editingCat ? String(editingCat.id) : null);
  const [name, setName] = useState(editingCat?.name ?? '');
  const [selectedCategory, setSelectedCategory] = useState<CategoryKey>('fur');
  const [saving, setSaving] = useState(false);

  const [prefilled, setPrefilled] = useState(Boolean(editingCat));
  useEffect(() => {
    if (prefilled || !editingCat) return;
    setConfiguration(normalizeConfiguration(editingCat.configuration));
    setCatId(String(editingCat.id));
    setName(editingCat.name);
    setPrefilled(true);
  }, [editingCat, prefilled]);

  const activeCategory = CATALOG.find((category) => category.key === selectedCategory) ?? CATALOG[0];
  const activeOptions = activeCategory.options;
  const colorCategory = COLOR_CATEGORIES.includes(selectedCategory as ConfigCategoryKey)
    ? selectedCategory as ConfigCategoryKey
    : null;
  const activeColor = colorCategory ? configuration[colorCategory].color ?? '#FCFCFC' : null;
  const activeHue = activeColor ? hueOf(activeColor) : 0;

  const pushHistory = (cfg: CatConfiguration) => {
    setHistory((prev) => [...prev.slice(-(MAX_HISTORY - 1)), cfg]);
  };

  const selectOption = (category: SingleCategory, code: string) => {
    if (configuration[category].code === code) return;
    pushHistory(configuration);
    setConfiguration({ ...configuration, [category]: keepColors(category, code, configuration) });
  };

  const toggleAccessory = (code: string) => {
    pushHistory(configuration);
    const group = accessoryByCode(code).group;
    setConfiguration((current) => {
      const selected = current.accessories.some((entry) => entry.code === code);
      const remaining = current.accessories.filter((entry) =>
        selected ? entry.code !== code : accessoryByCode(entry.code).group !== group,
      );
      return {
        ...current,
        accessories: selected ? remaining : [...remaining, { code, color: accessoryByCode(code).color }],
      };
    });
  };

  const clearAccessories = () => {
    if (configuration.accessories.length === 0) return;
    pushHistory(configuration);
    setConfiguration({ ...configuration, accessories: [] });
  };

  const changeColor = (category: ConfigCategoryKey, color: string) => {
    setConfiguration((current) => ({ ...current, [category]: { ...current[category], color } }));
  };

  const changeAccessoryColor = (code: string, color: string) => {
    setConfiguration((current) => ({
      ...current,
      accessories: current.accessories.map((entry) => (
        entry.code === code ? { ...entry, color } : entry
      )),
    }));
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
    const next = defaultConfig();
    for (const key of CONFIG_CATEGORY_KEYS) {
      const options = editorOptions(key);
      next[key] = categoryBlock(key, options[Math.floor(Math.random() * options.length)].code);
    }
    const accessories: CatConfiguration['accessories'] = [];
    const groups = new Set<string>();
    for (const option of ACCESSORIES) {
      if (groups.has(option.group) || Math.random() > 0.32) continue;
      groups.add(option.group);
      accessories.push({ code: option.code, color: option.color });
    }
    next.accessories = accessories;
    setConfiguration(next);
  };

  const handleSave = async () => {
    const clean = name.trim();
    if (!clean) return;
    setSaving(true);
    const saved = await saveCat(clean, configuration, catId);
    setSaving(false);
    if (saved) {
      setCatId(String(saved.id));
      if (editingId) navigate('/mis-gatos');
    }
  };

  return (
    <div className="screen-root screen-root--tight">
      <div className="editor-head">
        <h1 className="editor-title">{editingId ? 'Editar gato' : 'Crear gato'}</h1>
        <span className="mode-badge">{user ? 'En tu cuenta' : 'Modo invitado'}</span>
      </div>

      <section className="canvas-stage" aria-label="Vista previa del gato">
        <div className="canvas-stage__stars" aria-hidden="true" />
        <div className="canvas-stage__tools">
          <button type="button" className="canvas-btn" onClick={undo} disabled={history.length === 0} title="Deshacer" aria-label="Deshacer">
            <Undo2 size={17} strokeWidth={2.4} />
          </button>
          <button type="button" className="canvas-btn" onClick={reset} title="Reiniciar" aria-label="Reiniciar">
            <RotateCcw size={17} strokeWidth={2.4} />
          </button>
        </div>
        <button type="button" className="canvas-btn-amber canvas-stage__random" onClick={randomize} title="Combinación aleatoria">
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

      <label className="name-field">
        <span className="sr-only">Nombre del gato</span>
        <input
          className="name-field__input"
          placeholder="Nombre de tu gato..."
          value={name}
          maxLength={40}
          onChange={(event) => setName(event.target.value)}
          aria-label="Nombre del gato"
        />
        <span className="name-field__icon"><Pencil size={17} strokeWidth={2.2} /></span>
      </label>

      <div className="cat-carousel no-scrollbar" role="tablist" aria-label="Categorías">
        {CATALOG.map((category) => {
          const Icon = CATEGORY_ICONS[category.key as CategoryKey];
          const active = category.key === selectedCategory;
          return (
            <button
              key={category.key}
              type="button"
              role="tab"
              aria-selected={active}
              className="cat-chip"
              data-active={active}
              onClick={() => setSelectedCategory(category.key as CategoryKey)}
            >
              <Icon size={20} strokeWidth={2.2} aria-hidden="true" />
              <span className="cat-chip__label">{CATEGORY_LABELS[category.key as CategoryKey]}</span>
            </button>
          );
        })}
      </div>

      <div className="editor-section-head">
        <div>
          <h2 className="editor-section-title">{activeCategory.label}</h2>
          <p className="editor-section-copy">{activeCategory.tagline}</p>
        </div>
        {selectedCategory === 'accessory' && (
          <span className="editor-selection-count">{configuration.accessories.length} en uso</span>
        )}
      </div>

      {colorCategory && activeColor && (
        <div className="color-control">
          <div className="color-control__head">
            <label htmlFor="color-hue">Color de {CATEGORY_LABELS[colorCategory].toLowerCase()}</label>
            <span className="color-control__value">{activeColor}</span>
          </div>
          <input
            id="color-hue"
            className="color-control__slider"
            type="range"
            min="0"
            max="359"
            value={activeHue}
            aria-label={`Color de ${CATEGORY_LABELS[colorCategory].toLowerCase()}`}
            onPointerDown={() => pushHistory(configuration)}
            onKeyDown={() => pushHistory(configuration)}
            onChange={(event) => {
              const hue = Number(event.target.value);
              changeColor(colorCategory, colorAtHue(activeColor, hue));
            }}
          />
        </div>
      )}

      <div
        className="options-grid"
        role={selectedCategory === 'accessory' ? 'group' : 'listbox'}
        aria-label={`Opciones de ${activeCategory.label}`}
      >
        {selectedCategory === 'accessory' && (
          <button
            type="button"
            aria-pressed={configuration.accessories.length === 0}
            className="option-card option-card--clear"
            data-selected={configuration.accessories.length === 0}
            onClick={clearAccessories}
          >
            <span className="option-card__preview option-card__preview--clear" aria-hidden="true"><X size={24} strokeWidth={2.6} /></span>
            <span className="option-card__name">Ninguno</span>
          </button>
        )}
        {activeOptions.map((option) => {
          const selected = selectedCategory === 'accessory'
            ? configuration.accessories.some((entry) => entry.code === option.code)
            : configuration[selectedCategory as SingleCategory].code === option.code;
          const preview = previewFor(configuration, selectedCategory, option.code);

          if (selectedCategory === 'accessory') {
            const entry = configuration.accessories.find((item) => item.code === option.code);
            const color = entry?.color ?? accessoryByCode(option.code).color;
            return (
              <div
                key={option.code}
                className="option-card option-card--accessory"
                data-selected={selected}
              >
                <button
                  type="button"
                  className="option-card__select"
                  aria-pressed={selected}
                  title={option.description}
                  onClick={() => toggleAccessory(option.code)}
                >
                  <span className="option-card__preview" aria-hidden="true">
                    <CatSVG configuration={preview} size={58} />
                  </span>
                  <span className="option-card__name">{option.name}</span>
                  {selected && (
                    <span className="option-card__check" aria-hidden="true"><Check size={11} strokeWidth={4} /></span>
                  )}
                </button>
                {selected && (
                  <input
                    className="option-card__color"
                    type="range"
                    min="0"
                    max="359"
                    value={hueOf(color)}
                    aria-label={`Color de ${option.name}`}
                    aria-valuetext={color}
                    onPointerDown={() => pushHistory(configuration)}
                    onKeyDown={() => pushHistory(configuration)}
                    onChange={(event) => changeAccessoryColor(option.code, colorAtHue(color, Number(event.target.value)))}
                  />
                )}
              </div>
            );
          }

          return (
            <button
              key={option.code}
              type="button"
              role="option"
              aria-selected={selected}
              className="option-card"
              data-selected={selected}
              title={option.description}
              onClick={() => selectOption(selectedCategory as SingleCategory, option.code)}
            >
              <span className="option-card__preview" aria-hidden="true">
                <CatSVG configuration={preview} size={58} />
              </span>
              <span className="option-card__name">{option.name}</span>
              {selected && (
                <span className="option-card__check" aria-hidden="true"><Check size={11} strokeWidth={4} /></span>
              )}
            </button>
          );
        })}
      </div>

      <button type="button" className="save-btn" disabled={!name.trim() || saving} onClick={() => void handleSave()}>
        <Check size={22} strokeWidth={2.8} aria-hidden="true" />
        {saving ? 'Guardando…' : catId ? 'Guardar cambios' : 'Guardar gato'}
      </button>
    </div>
  );
}
