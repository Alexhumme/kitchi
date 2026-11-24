// Catálogo empaquetado y normalización de la configuración del gato.
// Los assets reales viven en assets/characters/ (ver characters.ts).
import {
  ACCESSORIES,
  BOTTOMS,
  DEFAULT_CODES,
  EYES,
  FURS,
  HAIRSTYLES,
  LEGACY_ALIASES,
  TOPWEAR,
  accessoryByCode,
  canonAssetCode,
  isAssetCode,
  type CharacterOption,
} from './characters';
import { isHexColor, normalizeHex } from './color';

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
  icon: string;
  tagline: string;
  options: CatalogOption[];
}

export const SCHEMA_VERSION = 1;

export type ConfigCategoryKey = 'fur' | 'eyes' | 'hair' | 'top' | 'bottom';
export type CategoryKey = ConfigCategoryKey | 'accessory';
export type ColorSlot = 'color' | 'base_color' | 'secondary_color';

export const CONFIG_CATEGORY_KEYS: ConfigCategoryKey[] = ['fur', 'eyes', 'hair', 'top', 'bottom'];
export const CATEGORY_KEYS: CategoryKey[] = [...CONFIG_CATEGORY_KEYS, 'accessory'];

const CATEGORY_META: Record<CategoryKey, Omit<CatalogCategory, 'key' | 'options'>> = {
  fur: { label: 'Pelaje', shortLabel: 'Pelaje', icon: 'palette', tagline: 'El color y patrón que envuelve al gato' },
  eyes: { label: 'Ojos', shortLabel: 'Ojos', icon: 'visibility', tagline: 'La mirada del mariscal' },
  hair: { label: 'Cabello', shortLabel: 'Cabello', icon: 'content_cut', tagline: 'El peinado: largo, corto o con flequillo' },
  top: { label: 'Parte superior', shortLabel: 'Superior', icon: 'dry_cleaning', tagline: 'Camisas, polos y chaquetas' },
  bottom: { label: 'Parte inferior', shortLabel: 'Inferior', icon: 'checkroom', tagline: 'Pantalones y faldas' },
  accessory: { label: 'Accesorios', shortLabel: 'Extras', icon: 'star', tagline: 'Combina accesorios sin repetir su tipo' },
};

function toOption(option: CharacterOption): CatalogOption {
  return { code: option.code, name: option.label, description: option.description, swatch: option.color };
}

export const CATALOG: CatalogCategory[] = [
  { key: 'fur', ...CATEGORY_META.fur, options: FURS.map(toOption) },
  { key: 'eyes', ...CATEGORY_META.eyes, options: EYES.map(toOption) },
  { key: 'hair', ...CATEGORY_META.hair, options: HAIRSTYLES.map(toOption) },
  { key: 'top', ...CATEGORY_META.top, options: TOPWEAR.map(toOption) },
  { key: 'bottom', ...CATEGORY_META.bottom, options: BOTTOMS.map(toOption) },
  { key: 'accessory', ...CATEGORY_META.accessory, options: ACCESSORIES.map(toOption) },
];

export const COLOR_KEYS: Record<CategoryKey, ColorSlot[]> = {
  fur: ['base_color', 'secondary_color'],
  eyes: ['color'],
  hair: ['color'],
  top: ['color'],
  bottom: ['color'],
  accessory: ['color'],
};

export interface CategoryBlock {
  code: string;
  color?: string;
  base_color?: string;
  secondary_color?: string;
}

export interface CatConfiguration {
  schema_version: number;
  fur: CategoryBlock;
  eyes: CategoryBlock;
  hair: CategoryBlock;
  top: CategoryBlock;
  bottom: CategoryBlock;
  accessories: CategoryBlock[];
}

function defaultColors(key: ConfigCategoryKey, code: string): Partial<Record<ColorSlot, string>> {
  if (key === 'fur') {
    const fur = FURS.find((option) => option.code === code) ?? FURS[0];
    return { base_color: fur.color, secondary_color: fur.secondary };
  }
  if (key === 'eyes') {
    const eyes = EYES.find((option) => option.code === code) ?? EYES[0];
    return { color: eyes.color };
  }
  if (key === 'hair') {
    const hair = HAIRSTYLES.find((option) => option.code === code) ?? HAIRSTYLES[0];
    return { color: hair.color };
  }
  if (key === 'top') {
    const top = TOPWEAR.find((option) => option.code === code) ?? TOPWEAR[0];
    return { color: top.color };
  }
  const bottom = BOTTOMS.find((option) => option.code === code) ?? BOTTOMS[0];
  return { color: bottom.color };
}

export function categoryBlock(key: ConfigCategoryKey, code: string): CategoryBlock {
  return { code, ...defaultColors(key, code) };
}

function blockFor(key: ConfigCategoryKey, code: string): CategoryBlock {
  return categoryBlock(key, code);
}

export function defaultConfig(): CatConfiguration {
  return {
    schema_version: SCHEMA_VERSION,
    fur: blockFor('fur', DEFAULT_CODES.fur),
    eyes: blockFor('eyes', DEFAULT_CODES.eyes),
    hair: blockFor('hair', DEFAULT_CODES.hair),
    top: blockFor('top', DEFAULT_CODES.top),
    bottom: blockFor('bottom', DEFAULT_CODES.bottom),
    accessories: [{ code: DEFAULT_CODES.accessory, color: accessoryByCode(DEFAULT_CODES.accessory).color }],
  };
}

export function canonCode(key: CategoryKey, code: string): string {
  if (key === 'fur') return FURS.some((fur) => fur.code === code) ? code : DEFAULT_CODES.fur;
  if (key === 'eyes') return EYES.some((eye) => eye.code === code) ? code : DEFAULT_CODES.eyes;
  return canonAssetCode(key, code);
}

export function isKnownCode(key: CategoryKey, code: string): boolean {
  if (key === 'fur') return FURS.some((fur) => fur.code === code);
  if (key === 'eyes') return EYES.some((eye) => eye.code === code);
  return isAssetCode(key, code);
}

export function getOption(category: string, code: string): CatalogOption | undefined {
  const key = category as CategoryKey;
  const list = CATALOG.find((item) => item.key === key);
  if (!list) return undefined;
  return list.options.find((option) => option.code === canonCode(key, code));
}

export function isValidOption(category: string, code: string): boolean {
  return Boolean(getOption(category, code));
}

function isAcceptedCode(key: CategoryKey, code: string): boolean {
  if (isKnownCode(key, code)) return true;
  if (key === 'fur' || key === 'eyes') return false;
  return Boolean(LEGACY_ALIASES[key]?.[code]);
}

export function editorOptions(key: CategoryKey): CatalogOption[] {
  return CATALOG.find((category) => category.key === key)?.options ?? [];
}

let apiCodes: Partial<Record<CategoryKey, Set<string>>> = {};
let source: 'bundled' | 'api' = 'bundled';

export function applyApiCatalog(payload: unknown): boolean {
  if (!payload || typeof payload !== 'object') return false;
  const categories = (payload as Record<string, unknown>)['categories'];
  if (!categories || typeof categories !== 'object') return false;
  const entries = categories as Record<string, unknown>;
  const next: Partial<Record<CategoryKey, Set<string>>> = {};
  let found = 0;
  for (const key of CATEGORY_KEYS) {
    const list = entries[key];
    if (!Array.isArray(list)) continue;
    const codes = new Set<string>();
    for (const raw of list) {
      if (!raw || typeof raw !== 'object') continue;
      const code = String((raw as Record<string, unknown>)['code'] ?? '').trim();
      if (code) codes.add(code);
    }
    if (codes.size) {
      next[key] = codes;
      found += 1;
    }
  }
  if (!found) return false;
  apiCodes = next;
  source = 'api';
  return true;
}

export function catalog(): CatalogCategory[] {
  return CATALOG;
}

export function sourceOf(): 'bundled' | 'api' {
  return source;
}

export function apiCodesOf(key: CategoryKey): string[] {
  return [...(apiCodes[key] ?? [])];
}

function readRawCode(block: unknown): string {
  if (typeof block === 'string') return block.trim();
  if (block && typeof block === 'object') {
    const value = (block as Record<string, unknown>)['style']
      ?? (block as Record<string, unknown>)['code']
      ?? (block as Record<string, unknown>)['pattern'];
    return typeof value === 'string' ? value.trim() : '';
  }
  return '';
}

function normalizeBlock(key: ConfigCategoryKey, raw: unknown): CategoryBlock {
  const code = canonCode(key, readRawCode(raw));
  const defaults = defaultColors(key, code);
  const rawObject = raw && typeof raw === 'object' ? raw as Record<string, unknown> : {};
  const block: CategoryBlock = { code };
  for (const slot of COLOR_KEYS[key]) {
    block[slot] = normalizeHex(rawObject[slot], defaults[slot] ?? '#FCFCFC');
  }
  return block;
}

function normalizeAccessories(raw: unknown): CategoryBlock[] {
  let entries: unknown;
  if (Array.isArray(raw)) {
    entries = raw;
  } else if (raw && typeof raw === 'object' && 'accessories' in raw) {
    entries = (raw as Record<string, unknown>)['accessories'];
  } else if (raw && typeof raw === 'object' && 'accessory' in raw) {
    const legacy = (raw as Record<string, unknown>)['accessory'];
    entries = Array.isArray(legacy) ? legacy : [legacy];
  } else {
    entries = [{ code: DEFAULT_CODES.accessory }];
  }

  if (!Array.isArray(entries)) return [{ code: DEFAULT_CODES.accessory }];
  const accessories: CategoryBlock[] = [];
  const codes = new Set<string>();
  const groups = new Set<string>();
  for (const entry of entries) {
    const rawCode = readRawCode(entry);
    if (!isAcceptedCode('accessory', rawCode)) continue;
    const code = canonCode('accessory', rawCode);
    const group = accessoryByCode(code).group;
    if (codes.has(code) || groups.has(group)) continue;
    codes.add(code);
    groups.add(group);
    const rawObject = entry && typeof entry === 'object' ? entry as Record<string, unknown> : {};
    const color = normalizeHex(rawObject['color'], accessoryByCode(code).color);
    accessories.push({ code, color });
  }
  return accessories;
}

export function normalizeConfiguration(raw: unknown): CatConfiguration {
  const source = raw && typeof raw === 'object' ? raw as Record<string, unknown> : {};
  return {
    schema_version: SCHEMA_VERSION,
    fur: normalizeBlock('fur', source['fur']),
    eyes: normalizeBlock('eyes', source['eyes']),
    hair: normalizeBlock('hair', source['hair']),
    top: normalizeBlock('top', source['top']),
    bottom: normalizeBlock('bottom', source['bottom']),
    accessories: normalizeAccessories(source),
  };
}

export function toApiConfiguration(config: CatConfiguration): Record<string, unknown> {
  const payload: Record<string, unknown> = { schema_version: SCHEMA_VERSION };
  for (const key of CONFIG_CATEGORY_KEYS) {
    const block = config[key];
    const entry: Record<string, string> = { code: block.code };
    for (const slot of COLOR_KEYS[key]) entry[slot] = block[slot] ?? '';
    payload[key] = entry;
  }
  payload['accessories'] = config.accessories.map((block) => (
    block.color ? { code: block.code, color: block.color } : { code: block.code }
  ));
  return payload;
}

export function validateConfig(config: unknown): string[] {
  const errors: string[] = [];
  if (!config || typeof config !== 'object') return ['La configuración debe ser un objeto.'];
  const obj = config as Record<string, unknown>;
  if (obj['schema_version'] !== SCHEMA_VERSION) errors.push('schema_version incompatible.');
  const allowed = new Set(['schema_version', ...CONFIG_CATEGORY_KEYS, 'accessories']);
  for (const key of Object.keys(obj)) {
    if (!allowed.has(key)) errors.push(`${key}: clave no permitida.`);
  }

  for (const key of CONFIG_CATEGORY_KEYS) {
    const block = obj[key];
    if (!block || typeof block !== 'object') {
      errors.push(`${key}: falta la categoría.`);
      continue;
    }
    const entry = block as Record<string, unknown>;
    const code = typeof entry['code'] === 'string' ? entry['code'] : '';
    if (!isAcceptedCode(key, code)) errors.push(`${key}: opción "${code}" inválida o inexistente.`);
    for (const slot of COLOR_KEYS[key]) {
      if (!isHexColor(entry[slot])) errors.push(`${key}.${slot}: color hexadecimal inválido.`);
    }
    for (const slot of Object.keys(entry)) {
      if (slot !== 'code' && !COLOR_KEYS[key].includes(slot as ColorSlot)) {
        errors.push(`${key}.${slot}: color no permitido en esta categoría.`);
      }
    }
  }

  const accessories = obj['accessories'];
  if (!Array.isArray(accessories)) {
    errors.push('accessories: falta la lista de accesorios.');
    return errors;
  }
  const codes = new Set<string>();
  const groups = new Set<string>();
  for (const [index, raw] of accessories.entries()) {
    if (!raw || typeof raw !== 'object') {
      errors.push(`accessories[${index}]: debe ser un objeto.`);
      continue;
    }
    const entry = raw as Record<string, unknown>;
    const code = typeof entry['code'] === 'string' ? entry['code'] : '';
    if (!isAcceptedCode('accessory', code)) {
      errors.push(`accessories[${index}]: opción "${code}" inválida o inexistente.`);
      continue;
    }
    const canonical = canonCode('accessory', code);
    const group = accessoryByCode(canonical).group;
    if (codes.has(canonical)) errors.push(`accessories[${index}]: accesorio repetido.`);
    if (groups.has(group)) errors.push(`accessories[${index}]: ya hay un accesorio de tipo ${group}.`);
    for (const slot of COLOR_KEYS.accessory) {
      if (entry[slot] !== undefined && !isHexColor(entry[slot])) {
        errors.push(`accessories[${index}].${slot}: color hexadecimal inválido.`);
      }
    }
    for (const slot of Object.keys(entry)) {
      if (slot !== 'code' && !COLOR_KEYS.accessory.includes(slot as ColorSlot)) {
        errors.push(`accessories[${index}].${slot}: campo no permitido.`);
      }
    }
    codes.add(canonical);
    groups.add(group);
  }
  return errors;
}
