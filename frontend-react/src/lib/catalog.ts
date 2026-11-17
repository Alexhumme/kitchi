// Catálogo empaquetado como fallback y validación local.
// La API (`/api/catalog/`) reemplaza estos valores cuando está disponible.

export interface CatalogOption {
  code: string;
  name: string;
  description: string;
  swatch: string;
  asset_path?: string;
  is_premium?: boolean;
}

export interface CatalogCategory {
  key: string;
  label: string;
  shortLabel: string;
  icon: string; // Material symbol name (font)
  tagline: string;
  options: CatalogOption[];
}

export const SCHEMA_VERSION = 1;

export const CATALOG: CatalogCategory[] = [
  {
    key: 'fur',
    label: 'Pelaje',
    shortLabel: 'Sup.',
    icon: 'palette',
    tagline: 'El color y patrón que envuelve al gato',
    options: [
      { code: 'tabby', name: 'Atigrado naranja', description: 'Rayas con actitud de lunes', swatch: '#F2A15A' },
      { code: 'bicolor', name: 'Bicolor', description: 'Mitad y mitad, como su personalidad', swatch: '#FFF0D8' },
      { code: 'dark_spots', name: 'Manchas oscuras', description: 'Manchas oscuras sobre fondo cálido', swatch: '#3A2C1F' },
    ],
  },
  {
    key: 'eyes',
    label: 'Ojos',
    shortLabel: 'Inf.',
    icon: 'visibility',
    tagline: 'La mirada del mariscal',
    options: [
      { code: 'round_green', name: 'Redondos verdes', description: 'Ojos redondos color bosque', swatch: '#4DAD72' },
      { code: 'big_blue', name: 'Grandes azules', description: 'Azul big y expresivos', swatch: '#6C8CFF' },
      { code: 'almond_amber', name: 'Almendrados ámbar', description: 'Almendrados ámbar con fuego', swatch: '#E8B94A' },
    ],
  },
  {
    key: 'hair',
    label: 'Cabello',
    shortLabel: 'Sup.',
    icon: 'content_cut',
    tagline: 'El peinado: flequillo corto, mechones o wavy',
    options: [
      { code: 'short_fringe', name: 'Flequillo corto', description: 'Fleco recto y ordenado', swatch: '#684632' },
      { code: 'side_locks', name: 'Mechones laterales', description: 'Mechones que caen a los lados', swatch: '#3A2C1F' },
      { code: 'wavy', name: 'Cabello ondulado', description: 'Ondas suaves y alborotadas', swatch: '#2C1F16' },
    ],
  },
  {
    key: 'top',
    label: 'Parte superior',
    shortLabel: 'Sup.',
    icon: 'dry_cleaning',
    tagline: 'Parte superior',
    options: [
      { code: 'tshirt', name: 'Camiseta', description: 'Camiseta lisa de algodón', swatch: '#70D6C1' },
      { code: 'hoodie', name: 'Sudadera', description: 'Sudadera con capucha', swatch: '#7B61FF' },
      { code: 'shirt', name: 'Camisa', description: 'Camisa de emergencia', swatch: '#FFB997' },
    ],
  },
  {
    key: 'bottom',
    label: 'Parte inferior',
    shortLabel: 'Inf.',
    icon: 'checkroom',
    tagline: 'Parte inferior',
    options: [
      { code: 'shorts', name: 'Pantalón corto', description: 'Bermudas cómodas', swatch: '#E45555' },
      { code: 'skirt', name: 'Falda', description: 'Falda corta con vuelo', swatch: '#FF8FAB' },
      { code: 'pants', name: 'Pantalón largo', description: 'Pantalón entero', swatch: '#2F9E8B' },
    ],
  },
  {
    key: 'accessory',
    label: 'Accesorios',
    shortLabel: 'Extra',
    icon: 'star',
    tagline: 'El plus que remata el look',
    options: [
      { code: 'glasses', name: 'Gafas', description: 'Gafas redondas estilo intelectual', swatch: '#211B26' },
      { code: 'bow', name: 'Lazo', description: 'Lazo rojo clásico', swatch: '#D64545' },
      { code: 'beanie', name: 'Gorro', description: 'Gorro de lana a rayas', swatch: '#FFD166' },
    ],
  },
];

export interface CatConfiguration {
  schema_version: number;
  fur: string;
  eyes: string;
  hair: string;
  top: string;
  bottom: string;
  accessory: string;
}

export function defaultConfig(): CatConfiguration {
  const cfg: Record<string, unknown> = { schema_version: SCHEMA_VERSION };
  for (const cat of CATALOG) {
    cfg[cat.key] = cat.options[0].code;
  }
  return cfg as unknown as CatConfiguration;
}

export function getOption(category: string, code: string): CatalogOption | undefined {
  return CATALOG.find((c) => c.key === category)?.options.find((o) => o.code === code);
}

export function isValidOption(category: string, code: string): boolean {
  return Boolean(getOption(category, code));
}

const DEFAULT_CATEGORIES_FALLBACK = [...CATALOG];
let overrideCategories: CatalogCategory[] = CATALOG;
let source: 'bundled' | 'api' = 'bundled';

export function applyApiCatalog(payload: unknown): boolean {
  if (!payload || typeof payload !== 'object') return false;
  const obj = payload as Record<string, unknown>;
  const cats = obj['categories'];
  if (!cats || typeof cats !== 'object') return false;
  const entries = cats as Record<string, unknown>;
  const rebuilt: CatalogCategory[] = [];
  for (const base of DEFAULT_CATEGORIES_FALLBACK) {
    const arr = entries[base.key];
    if (!Array.isArray(arr) || arr.length === 0) return false;
    const options: CatalogOption[] = [];
    const seen = new Set<string>();
    for (const raw of arr) {
      if (!raw || typeof raw !== 'object') continue;
      const e = raw as Record<string, unknown>;
      const code = String(e['code'] ?? '').trim();
      if (!code || seen.has(code)) continue;
      seen.add(code);
      const bundled = base.options.find((o) => o.code === code);
      options.push(
        bundled ?? {
          code,
          name: String(e['label'] ?? e['name'] ?? code),
          description: String(e['description'] ?? ''),
          swatch: fallbackSwatch(base.key, code),
          asset_path: String(e['asset_path'] ?? ''),
          is_premium: Boolean(e['is_premium']),
        },
      );
    }
    if (options.length === 0) return false;
    rebuilt.push({ ...base, options });
  }
  overrideCategories = rebuilt;
  source = 'api';
  return true;
}

const FALLBACK_PALETTE = ['#F2A15A', '#FFB997', '#FFD166', '#70D6C1', '#7B61FF', '#FF8FAB', '#DBC6FF', '#FFF3DF'];
function hash(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = (h * 16777619) >>> 0; }
  return h;
}
function fallbackSwatch(key: string, code: string): string {
  return FALLBACK_PALETTE[hash(`${key}:${code}`) % FALLBACK_PALETTE.length];
}

export function catalog(): CatalogCategory[] {
  return overrideCategories;
}

export function sourceOf(): 'bundled' | 'api' {
  return source;
}

export function validateConfig(cfg: unknown): string[] {
  const errors: string[] = [];
  if (!cfg || typeof cfg !== 'object') return ['La configuración debe ser un objeto.'];
  const c = cfg as Record<string, unknown>;
  if (typeof c.schema_version !== 'number' || c.schema_version !== SCHEMA_VERSION) {
    errors.push('schema_version incompatible.');
  }
  for (const cat of CATALOG) {
    const value = c[cat.key];
    if (typeof value !== 'string' || !isValidOption(cat.key, value)) {
      errors.push(`${cat.key}: opción "${String(value)}" inválida o inexistente.`);
    }
  }
  return errors;
}

export function normalizeConfiguration(raw: unknown): CatConfiguration {
  if (!raw || typeof raw !== 'object') {
    const err = validateConfig(defaultConfig());
    void err;
    return defaultConfig();
  }
  const r = raw as Record<string, unknown>;
  const out: Record<string, string> = {};
  for (const cat of CATALOG) {
    const block = r[cat.key];
    let code = '';
    if (typeof block === 'string') code = block;
    else if (block && typeof block === 'object') {
      const b = block as Record<string, unknown>;
      code = String(b['code'] ?? b['style'] ?? b['pattern'] ?? '');
    }
    if (!isValidOption(cat.key, code)) code = cat.options[0].code;
    out[cat.key] = code;
  }
  return { ...out, schema_version: SCHEMA_VERSION } as CatConfiguration;
}
