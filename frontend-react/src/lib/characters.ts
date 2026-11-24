// Registro de los assets reales del personaje (diseñadora gráfica).
//
// - Cada SVG se importa como texto y se prepara una sola vez: sus clases
//   `.cls-N` de Illustrator se convierten en rellenos inline. Solo los rellenos
//   base de cabello/prendas y el amarillo del cuerpo se marcan para tintado;
//   los blancos de detalle (botones, brillos y lunas) conservan su color.
// - El cabello se compone en dos capas: la de atrás va detrás del cuerpo y la
//   de delante sobre la cara. Cada peinado declara su par back/front.
// - Los bounding boxes se midieron con el navegador (getBBox) y se guardan
//   aquí para poder anclar cada pieza sin depender del DOM en tiempo de render.
import { normalizeHex } from './color';

export const INK = '#211B26';
const BASE_FILE = 'base/avatar_predetermined.svg';
const HEAD_FILE = 'base/avatar_head.svg';
const SLOT = 'data-slot="1"';

export interface Bbox {
  x: number;
  y: number;
  w: number;
  h: number;
}

export interface PreparedAsset {
  key: string;
  inner: string;
  bbox: Bbox;
}

export interface Anchor {
  cx: number;
  top: number;
  width: number;
}

export interface CharacterOption {
  code: string;
  label: string;
  description: string;
  color: string;
}

export interface GarmentOption extends CharacterOption {
  file: string;
}

export interface HairOption extends CharacterOption {
  back: string;
  front: string;
}

export type AccessoryGroup = 'eyewear' | 'neckwear' | 'facial_hair' | 'pipe' | 'headwear' | 'hair_bows';

export interface AccessoryOption extends CharacterOption {
  file: string;
  anchor: Anchor;
  group: AccessoryGroup;
}

const BBOXES: Record<string, Bbox> = {
  'accessories/3_pointed_crown.svg': { x: 4.37, y: 8.26, w: 49.21, h: 37.76 },
  'accessories/4_pointed_crown.svg': { x: 4.46, y: 8.8, w: 51.19, h: 31 },
  'accessories/bow_tie.svg': { x: 9.72, y: 8.69, w: 54.75, h: 21.43 },
  'accessories/collar_tie.svg': { x: 5.72, y: 4.63, w: 58.88, h: 25.4 },
  'accessories/fedora_hat.svg': { x: 17.14, y: 5.26, w: 58.94, h: 41.88 },
  'accessories/glasses.svg': { x: 10.07, y: 4.98, w: 71.56, h: 36.31 },
  'accessories/hair_bows.svg': { x: 4.71, y: 8.41, w: 130.45, h: 48.17 },
  'accessories/long_bow_tie.svg': { x: 5.81, y: 5.48, w: 53.56, h: 56.33 },
  'accessories/moustache.svg': { x: 10.33, y: 6.04, w: 53.24, h: 16.98 },
  'accessories/piccolo_antennas.svg': { x: 6.39, y: 11.87, w: 124.58, h: 38.67 },
  'accessories/pipe.svg': { x: 21.73, y: 3.03, w: 49.64, h: 35.78 },
  'accessories/round_glasses.svg': { x: 6.81, y: 4.62, w: 60.3, h: 26.19 },
  'accessories/winter_beanie.svg': { x: 12.46, y: 3.46, w: 49.1, h: 51.8 },
  'base/avatar_head.svg': { x: 12.364, y: 9.129, w: 155.775, h: 80.071 },
  'base/avatar_predetermined.svg': { x: 5.64, y: 4.85, w: 190.71, h: 224.89 },
  'bottoms/denim_shorts.svg': { x: 6.05, y: 2.88, w: 123.77, h: 77.78 },
  'bottoms/flared_skirt.svg': { x: 5.49, y: 1.49, w: 159.04, h: 69.58 },
  'bottoms/greek_key_skirt.svg': { x: 4.88, y: 3.88, w: 168.06, h: 78.91 },
  'bottoms/long_trousers.svg': { x: 24.49, y: 2.87, w: 121, h: 77.42 },
  'bottoms/pleated_skirt.svg': { x: 3.38, y: 4.42, w: 136.53, h: 71.14 },
  'bottoms/sweat_pants.svg': { x: 9.2, y: 5.83, w: 138.05, h: 96.26 },
  'hair/anime_style_hair_back.svg': { x: 8.83, y: 5.75, w: 154.9, h: 99.99 },
  'hair/anime_style_hair_front.svg': { x: 8.61, y: 4.35, w: 96.86, h: 51.62 },
  'hair/bob_haircutwith_volume_at_the_back.svg': { x: 4.12, y: 6.27, w: 121.29, h: 110.1 },
  'hair/cloud_like_bangs_at_the_front.svg': { x: 5.59, y: 7.44, w: 102.99, h: 42.57 },
  'hair/hair_back_medium.svg': { x: 6.82, y: 7.97, w: 100.48, h: 84.66 },
  'hair/long_hair_in_the_back.svg': { x: 8.22, y: 4.97, w: 127.96, h: 210.34 },
  'hair/long_side_swept_bangs_in_the_front.svg': { x: 7.61, y: 4.8, w: 83.97, h: 59.56 },
  'hair/short_bangs_front.svg': { x: 4.97, y: 15.61, w: 112.15, h: 52.47 },
  'hair/short_hair_in_the_back.svg': { x: 4.19, y: 5.52, w: 106.81, h: 79.87 },
  'hair/short_hair_in_the_front.svg': { x: 5.89, y: 2.59, w: 93.38, h: 64.16 },
  'hair/side_swept_bangs.svg': { x: 8.69, y: 1.42, w: 95.95, h: 56.11 },
  'hair/triangular_fringe_at_the_front.svg': { x: 3.34, y: 6.73, w: 94.34, h: 39.37 },
  'hair/uneven_bangs_at_the_front.svg': { x: 6.61, y: 4.28, w: 95.81, h: 54.09 },
  'hair/widows_peak.svg': { x: 10.05, y: 2.49, w: 88.9, h: 58.28 },
  'tops/bib_front_shirt.svg': { x: 6.7, y: 5.59, w: 175.45, h: 83.75 },
  'tops/long_sleeved shirt.svg': { x: 2.65, y: 3.78, w: 172.22, h: 82.78 },
  'tops/long_sleeved_shirt_with_cuffs.svg': { x: 5.88, y: 7.6, w: 176.42, h: 83.18 },
  'tops/polo_shirt.svg': { x: 5.47, y: 5.13, w: 157.33, h: 96.11 },
  'tops/shirt with_zipper.svg': { x: 1.76, y: 1.81, w: 148.99, h: 92.33 },
  'tops/short_sleeved shirt.svg': { x: 12.11, y: 6.94, w: 152.69, h: 82.33 },
};

const COLORABLE_FILLS = new Set(['#fcfcfc', '#eae16a']);
const INK_FILLS = new Set(['#020203', '#0a0a0a', '#211b26']);

function extractInner(raw: string): string {
  const open = raw.indexOf('>', raw.indexOf('<svg'));
  const close = raw.lastIndexOf('</svg>');
  if (open < 0 || close < 0) return '';
  return raw.slice(open + 1, close);
}

function styleRules(css: string): Map<string, { fill?: string; stroke?: string }> {
  const rules = new Map<string, { fill?: string; stroke?: string }>();
  const block = /\.(cls-\d+)\s*\{([^}]*)\}/g;
  let match: RegExpExecArray | null;
  while ((match = block.exec(css))) {
    const declarations = match[2];
    const fill = /fill:\s*(#[0-9a-fA-F]{3,8}|none)/.exec(declarations)?.[1]?.toLowerCase();
    const stroke = /stroke:\s*(#[0-9a-fA-F]{3,8}|none)/.exec(declarations)?.[1]?.toLowerCase();
    rules.set(match[1], { fill, stroke });
  }
  return rules;
}

function prepare(raw: string, key: string): PreparedAsset {
  let inner = extractInner(raw);
  const rules = styleRules(inner);
  inner = inner.replace(/<defs>[\s\S]*?<\/defs>/g, '');
  inner = inner.replace(/<title>[\s\S]*?<\/title>/g, '');
  inner = inner.replace(/\sclass="(cls-\d+)"/g, (_full, cls: string) => {
    const rule = rules.get(cls);
    if (!rule) return '';
    let attrs = '';
    if (rule.fill === 'none') attrs += ' fill="none"';
    else if (rule.fill && COLORABLE_FILLS.has(rule.fill)) attrs += ` ${SLOT}`;
    else if (rule.fill && INK_FILLS.has(rule.fill)) attrs += ` fill="${INK}"`;
    else if (rule.fill) attrs += ` fill="${rule.fill}"`;
    if (rule.stroke && rule.stroke !== 'none') {
      attrs += ` stroke="${INK_FILLS.has(rule.stroke) ? INK : rule.stroke}"`;
    }
    return attrs;
  });
  // El cuerpo y la cabeza traen los dos ojos como rellenos negros independientes.
  // Se marcan para pintarlos con el color de la categoría "ojos" sin perder su forma.
  if (key === BASE_FILE || key === HEAD_FILE) {
    const eyeStart = key === BASE_FILE
      ? /d="M(?:80\.189|115\.643),62\.576/
      : /d="M(?:70\.973|106\.427),66\.858/;
    inner = inner.replace(/<path\b([^>]*?)\/>/g, (full, attrs: string) => {
      if (!eyeStart.test(attrs)) return full;
      return `<path${attrs.replace(/\sfill="[^"]*"/g, '')} data-eye="1" />`;
    });
  }
  return { key, inner, bbox: BBOXES[key] ?? { x: 0, y: 0, w: 1, h: 1 } };
}

// Vite inyecta el texto de cada SVG del repositorio. La carpeta `assets/` de la
// raíz es la fuente única de verdad (no se duplica en frontend-react/).
const RAW = import.meta.glob('../../../assets/characters/**/*.svg', {
  query: '?raw',
  import: 'default',
  eager: true,
}) as Record<string, string>;

const PREPARED = new Map<string, PreparedAsset>();
for (const [path, raw] of Object.entries(RAW)) {
  const key = path.match(/assets\/characters\/(.+)$/)?.[1] ?? path;
  PREPARED.set(key, prepare(raw, key));
}

const EMPTY: PreparedAsset = { key: '', inner: '', bbox: { x: 0, y: 0, w: 1, h: 1 } };

export function getAsset(file: string): PreparedAsset {
  return PREPARED.get(file) ?? EMPTY;
}

export function baseAsset(): PreparedAsset {
  return getAsset(BASE_FILE);
}

export function headAsset(): PreparedAsset {
  return getAsset(HEAD_FILE);
}

export function colorize(asset: PreparedAsset, color: string): string {
  const safe = normalizeHex(color, '#FCFCFC');
  return asset.inner.replaceAll(SLOT, `fill="${safe}"`);
}

/**
 * El cuerpo y la cabeza necesitan dos colores: el pelaje (rellenos amarillos) y
 * los ojos (paths marcados con `data-eye`). Al pintarlos se conserva su silueta.
 */
export function colorizeBase(asset: PreparedAsset, furColor: string, eyeColor: string): string {
  const safeFur = normalizeHex(furColor, '#F2A15A');
  const safeEye = normalizeHex(eyeColor, '#211B26');
  return asset.inner
    .replaceAll(SLOT, `fill="${safeFur}"`)
    .replaceAll('data-eye="1"', `fill="${safeEye}" data-eye="1"`);
}

export function placeTransform(asset: PreparedAsset, anchor: Anchor): string {
  const scale = anchor.width / asset.bbox.w;
  const tx = anchor.cx - (asset.bbox.x + asset.bbox.w / 2) * scale;
  const ty = anchor.top - asset.bbox.y * scale;
  return `translate(${tx.toFixed(3)} ${ty.toFixed(3)}) scale(${scale.toFixed(4)})`;
}

// ---------- Anclajes sobre el lienzo del gato (viewBox 206.068 × 270, desde y=-10) ----------
export const BASE_ANCHOR: Anchor = { cx: 98.09, top: 24.85, width: 190.71 };
export const HEAD_ANCHOR: Anchor = { cx: 97, top: 24.851, width: 155.781 };
export const HAIR_BACK_ANCHOR: Anchor = { cx: 94, top: -8, width: 148 };
export const HAIR_FRONT_ANCHOR: Anchor = { cx: 96, top: 30, width: 98 };
export const TOP_ANCHOR: Anchor = { cx: 94, top: 86, width: 170 };
export const BOTTOM_ANCHOR: Anchor = { cx: 92, top: 167, width: 120 };

// ---------- Catálogo de piezas ----------
export const HAIRSTYLES: HairOption[] = [
  {
    code: 'anime_style',
    label: 'Anime',
    description: 'Puntas largas y flequillo animado',
    color: '#6B4226',
    back: 'hair/anime_style_hair_back.svg',
    front: 'hair/anime_style_hair_front.svg',
  },
  {
    code: 'short_bangs',
    label: 'Flequillo corto',
    description: 'Fleco recto y ordenado',
    color: '#3A2C1F',
    back: 'hair/short_hair_in_the_back.svg',
    front: 'hair/short_bangs_front.svg',
  },
  {
    code: 'cloud_bangs',
    label: 'Nube',
    description: 'Flequillo redondeado y suave',
    color: '#8A5A34',
    back: 'hair/hair_back_medium.svg',
    front: 'hair/cloud_like_bangs_at_the_front.svg',
  },
  {
    code: 'long_side',
    label: 'Largo lateral',
    description: 'Melena larga con mechón lateral',
    color: '#2C1F16',
    back: 'hair/long_hair_in_the_back.svg',
    front: 'hair/long_side_swept_bangs_in_the_front.svg',
  },
  {
    code: 'short_hair',
    label: 'Corto',
    description: 'Corte corto con volumen',
    color: '#5A3A22',
    back: 'hair/short_hair_in_the_back.svg',
    front: 'hair/short_hair_in_the_front.svg',
  },
  {
    code: 'side_swept',
    label: 'Barrido',
    description: 'Flequillo barrido hacia un lado',
    color: '#7A4A2A',
    back: 'hair/hair_back_medium.svg',
    front: 'hair/side_swept_bangs.svg',
  },
  {
    code: 'triangular',
    label: 'Triangular',
    description: 'Puntas geométricas al frente',
    color: '#4A3220',
    back: 'hair/short_hair_in_the_back.svg',
    front: 'hair/triangular_fringe_at_the_front.svg',
  },
  {
    code: 'uneven',
    label: 'Desigual',
    description: 'Flequillo despuntado y relajado',
    color: '#6A4628',
    back: 'hair/hair_back_medium.svg',
    front: 'hair/uneven_bangs_at_the_front.svg',
  },
  {
    code: 'widows_peak',
    label: 'Pico de viuda',
    description: 'Entrada marcada en el centro',
    color: '#382A1E',
    back: 'hair/short_hair_in_the_back.svg',
    front: 'hair/widows_peak.svg',
  },
  {
    code: 'bob',
    label: 'Bob',
    description: 'Melena bob con volumen atrás',
    color: '#513722',
    back: 'hair/bob_haircutwith_volume_at_the_back.svg',
    front: 'hair/short_bangs_front.svg',
  },
];

export const TOPWEAR: GarmentOption[] = [
  {
    code: 'polo_shirt',
    label: 'Camisa polo',
    description: 'Cuello y botones, look clásico',
    color: '#7B61FF',
    file: 'tops/polo_shirt.svg',
  },
  {
    code: 'short_sleeved',
    label: 'Manga corta',
    description: 'Camiseta ligera de diario',
    color: '#70D6C1',
    file: 'tops/short_sleeved shirt.svg',
  },
  {
    code: 'long_sleeved',
    label: 'Manga larga',
    description: 'Camisa de manga larga',
    color: '#FFB997',
    file: 'tops/long_sleeved shirt.svg',
  },
  {
    code: 'cuffed_shirt',
    label: 'Puños',
    description: 'Manga con puños y bolsillos',
    color: '#F4A261',
    file: 'tops/long_sleeved_shirt_with_cuffs.svg',
  },
  {
    code: 'bib_shirt',
    label: 'Bordada',
    description: 'Camisa con bordado en el pecho',
    color: '#E76F51',
    file: 'tops/bib_front_shirt.svg',
  },
  {
    code: 'zipper_shirt',
    label: 'Cremallera',
    description: 'Chaqueta con cremallera',
    color: '#457B9D',
    file: 'tops/shirt with_zipper.svg',
  },
];

export const BOTTOMS: GarmentOption[] = [
  {
    code: 'denim_shorts',
    label: 'Pantalón corto',
    description: 'Vaqueros cómodos',
    color: '#4D7EA8',
    file: 'bottoms/denim_shorts.svg',
  },
  {
    code: 'long_trousers',
    label: 'Pantalón largo',
    description: 'Pantalón de vestir',
    color: '#2F9E8B',
    file: 'bottoms/long_trousers.svg',
  },
  {
    code: 'sweat_pants',
    label: 'Deportivo',
    description: 'Pantalón con cordón y bolsillos',
    color: '#7B61FF',
    file: 'bottoms/sweat_pants.svg',
  },
  {
    code: 'flared_skirt',
    label: 'Acampanada',
    description: 'Falda con vuelo amplio',
    color: '#FF8FAB',
    file: 'bottoms/flared_skirt.svg',
  },
  {
    code: 'greek_key_skirt',
    label: 'Griega',
    description: 'Falda con detalle de greca',
    color: '#F4A261',
    file: 'bottoms/greek_key_skirt.svg',
  },
  {
    code: 'pleated_skirt',
    label: 'Plisada',
    description: 'Falda de tablas clásica',
    color: '#E76F51',
    file: 'bottoms/pleated_skirt.svg',
  },
];

export const ACCESSORIES: AccessoryOption[] = [
  {
    code: 'round_glasses',
    label: 'Gafas redondas',
    description: 'Intelectual, claramente',
    color: '#FCFCFC',
    file: 'accessories/round_glasses.svg',
    anchor: { cx: 96, top: 58, width: 58 },
    group: 'eyewear',
  },
  {
    code: 'big_glasses',
    label: 'Gafas grandes',
    description: 'Montura ancha con estilo',
    color: '#fd8b65',
    file: 'accessories/glasses.svg',
    anchor: { cx: 94, top: 51, width: 66 },
    group: 'eyewear',
  },
  {
    code: 'bow_tie',
    label: 'Corbata de lazo',
    description: 'Lazo clásico al cuello',
    color: '#FCFCFC',
    file: 'accessories/bow_tie.svg',
    anchor: { cx: 94, top: 92, width: 44 },
    group: 'neckwear',
  },
  {
    code: 'collar_tie',
    label: 'Corbata',
    description: 'Corbata formal',
    color: '#7b7b7b',
    file: 'accessories/collar_tie.svg',
    anchor: { cx: 96, top: 98, width: 42 },
    group: 'neckwear',
  },
  {
    code: 'long_bow_tie',
    label: 'Corbata larga',
    description: 'Corbata de lazo caída',
    color: '#363636',
    file: 'accessories/long_bow_tie.svg',
    anchor: { cx: 96, top: 98, width: 40 },
    group: 'neckwear',
  },
  {
    code: 'moustache',
    label: 'Bigote',
    description: 'Bigote de caballero',
    color: '#633a08',
    file: 'accessories/moustache.svg',
    anchor: { cx: 94, top: 82, width: 40 },
    group: 'facial_hair',
  },
  {
    code: 'pipe',
    label: 'Pipa',
    description: 'Pipa de detective',
    color: '#6e4311',
    file: 'accessories/pipe.svg',
    anchor: { cx: 79, top: 89, width: 38 },
    group: 'pipe',
  },
  {
    code: 'fedora',
    label: 'Sombrero',
    description: 'Fedora con cinta',
    color: '#b1afaf',
    file: 'accessories/fedora_hat.svg',
    anchor: { cx: 91, top: 10, width: 70 },
    group: 'headwear',
  },
  {
    code: 'winter_beanie',
    label: 'Gorro de lana',
    description: 'Gorro tejido para el frío',
    color: '#a0e0f6',
    file: 'accessories/winter_beanie.svg',
    anchor: { cx: 94, top: -14, width: 64 },
    group: 'headwear',
  },
  {
    code: 'three_pointed_crown',
    label: 'Corona de 3',
    description: 'Corona de tres puntas',
    color: '#f0d250',
    file: 'accessories/3_pointed_crown.svg',
    anchor: { cx: 94, top: 12, width: 54 },
    group: 'headwear',
  },
  {
    code: 'four_pointed_crown',
    label: 'Corona de 4',
    description: 'Corona de cuatro puntas',
    color: '#f6d52f',
    file: 'accessories/4_pointed_crown.svg',
    anchor: { cx: 94, top: 10, width: 56 },
    group: 'headwear',
  },
  {
    code: 'hair_bows',
    label: 'Lazos',
    description: 'Par de lazos para el pelo',
    color: '#f7a7a7',
    file: 'accessories/hair_bows.svg',
    anchor: { cx: 98, top: 26, width: 110 },
    group: 'hair_bows',
  },
  {
    code: 'piccolo_antennas',
    label: 'Antenas',
    description: 'Antenas de otro planeta',
    color: '#159b48',
    file: 'accessories/piccolo_antennas.svg',
    anchor: { cx: 98, top: 40, width: 126 },
    group: 'headwear',
  },
];

// Pelaje y ojos se dibujan por código (no hay assets sueltos en la entrega).
export interface FurOption extends CharacterOption {
  secondary: string;
}

export const FURS: FurOption[] = [
  { code: 'tabby', label: 'Atigrado naranja', description: 'Rayas con actitud de lunes', color: '#F2A15A', secondary: '#FFF0D8' },
  { code: 'bicolor', label: 'Bicolor', description: 'Mitad y mitad, como su personalidad', color: '#FFF0D8', secondary: '#F2A15A' },
  { code: 'dark_spots', label: 'Manchas oscuras', description: 'Manchas oscuras sobre fondo cálido', color: '#3A2C1F', secondary: '#6B4A2E' },
];

export const EYES: CharacterOption[] = [
  { code: 'round_green', label: 'Redondos verdes', description: 'Ojos redondos color bosque', color: '#4DAD72' },
  { code: 'big_blue', label: 'Grandes azules', description: 'Azul big y expresivos', color: '#6C8CFF' },
  { code: 'almond_amber', label: 'Almendrados ámbar', description: 'Almendrados ámbar con fuego', color: '#E8B94A' },
];

export const DEFAULT_CODES = {
  fur: 'tabby',
  eyes: 'round_green',
  hair: 'anime_style',
  top: 'polo_shirt',
  bottom: 'long_trousers',
  accessory: 'round_glasses',
} as const;

// Códigos del catálogo provisional que siguen existiendo en la API y en gatos
// antiguos: se traducen al asset real más cercano sin tocar el backend.
export const LEGACY_ALIASES: Record<'hair' | 'top' | 'bottom' | 'accessory', Record<string, string>> = {
  hair: { short_fringe: 'short_bangs', side_locks: 'side_swept', wavy: 'cloud_bangs' },
  top: { tshirt: 'short_sleeved', hoodie: 'cuffed_shirt', shirt: 'polo_shirt' },
  bottom: { shorts: 'denim_shorts', skirt: 'pleated_skirt', pants: 'long_trousers' },
  accessory: { glasses: 'round_glasses', bow: 'bow_tie', beanie: 'winter_beanie' },
};

export function hairByCode(code: string): HairOption {
  return HAIRSTYLES.find((h) => h.code === code) ?? HAIRSTYLES[0];
}

export function topByCode(code: string): GarmentOption {
  return TOPWEAR.find((t) => t.code === code) ?? TOPWEAR[0];
}

export function bottomByCode(code: string): GarmentOption {
  return BOTTOMS.find((b) => b.code === code) ?? BOTTOMS[0];
}

export function accessoryByCode(code: string): AccessoryOption {
  return ACCESSORIES.find((a) => a.code === code) ?? ACCESSORIES[0];
}

export function canonAssetCode(
  category: 'hair' | 'top' | 'bottom' | 'accessory',
  code: string,
): string {
  const list =
    category === 'hair' ? HAIRSTYLES : category === 'top' ? TOPWEAR : category === 'bottom' ? BOTTOMS : ACCESSORIES;
  if (list.some((o) => o.code === code)) return code;
  return LEGACY_ALIASES[category][code] ?? DEFAULT_CODES[category];
}

export function isAssetCode(category: 'hair' | 'top' | 'bottom' | 'accessory', code: string): boolean {
  const list =
    category === 'hair' ? HAIRSTYLES : category === 'top' ? TOPWEAR : category === 'bottom' ? BOTTOMS : ACCESSORIES;
  return list.some((o) => o.code === code);
}
