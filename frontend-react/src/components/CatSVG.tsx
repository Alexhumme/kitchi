// Gato chibi dibujado como SVG a partir de la configuración del catálogo.
// Sustituye al placeholder de contenedores de Flet: aquí se dibuja el
// conjunto completo (pelaje, cara, peinado, ropa y accesorio).
import { getOption, normalizeConfiguration } from '../lib/catalog';

const INK = '#211B26';

interface Props {
  configuration: unknown;
  size?: number;
  className?: string;
}

export default function CatSVG({ configuration, size = 200, className }: Props) {
  const cfg = normalizeConfiguration(configuration);
  const fur = getOption('fur', cfg.fur)?.swatch ?? '#F2A15A';
  const eyesCode = cfg.eyes;
  const hairCode = cfg.hair;
  const topCode = cfg.top;
  const bottomCode = cfg.bottom;
  const accessoryCode = cfg.accessory;
  const hairSwatch = getOption('hair', hairCode)?.swatch ?? '#684632';

  const height = (size * 300) / 220;
  const stroke = 3;

  // ---------- pelaje ----------
  const isBicolor = cfg.fur === 'bicolor';
  const isDarkSpots = cfg.fur === 'dark_spots';
  const innerEar = isBicolor ? '#F7C9A0' : '#FFD9C4';
  const muzzle = '#FFE6C7';

  const tabbyStripes = cfg.fur === 'tabby' ? (
    <g stroke="#D97F3C" strokeWidth={5} strokeLinecap="round">
      <line x1="98" y1="76" x2="98" y2="90" />
      <line x1="110" y1="74" x2="110" y2="90" />
      <line x1="122" y1="76" x2="122" y2="90" />
      <line x1="52" y1="122" x2="66" y2="126" />
      <line x1="50" y1="136" x2="64" y2="136" />
      <line x1="168" y1="122" x2="154" y2="126" />
      <line x1="170" y1="136" x2="156" y2="136" />
    </g>
  ) : null;

  const bicolorPatch = isBicolor ? (
    <path
      d="M46,108 C44,62 78,44 110,44 C96,66 96,86 104,104 C86,104 66,116 54,138 C48,128 46,118 46,108 Z"
      fill="#F2A15A"
      stroke={INK}
      strokeWidth={stroke}
      strokeLinejoin="round"
    />
  ) : null;

  const darkSpots = isDarkSpots ? (
    <g fill="#3A2C1F">
      <ellipse cx="74" cy="80" rx="9" ry="5.5" transform="rotate(-18 74 80)" />
      <ellipse cx="150" cy="78" rx="9" ry="5.5" transform="rotate(18 150 78)" />
      <ellipse cx="64" cy="128" rx="8" ry="5" transform="rotate(-12 64 128)" />
      <ellipse cx="160" cy="128" rx="8" ry="5" transform="rotate(12 160 128)" />
      <ellipse cx="110" cy="66" rx="7" ry="4" />
    </g>
  ) : null;

  // ---------- ojos ----------
  const eye = (cx: number, flip: 1 | -1) => {
    const base = { stroke: INK, strokeWidth: 2.5 } as const;
    if (eyesCode === 'almond_amber') {
      return (
        <g transform={`rotate(${flip * -7} ${cx} 112)`}>
          <ellipse cx={cx} cy={112} rx={14} ry={7.6} fill="#E8B94A" {...base} />
          <ellipse cx={cx} cy={112} rx={4.4} ry={6.4} fill={INK} />
          <circle cx={cx - 4} cy={109} r={1.6} fill="#FFFFFF" />
        </g>
      );
    }
    const big = eyesCode === 'big_blue';
    const r = big ? 13 : 11;
    const fill = big ? '#6C8CFF' : '#4DAD72';
    return (
      <g>
        <ellipse cx={cx} cy={112} rx={r} ry={r} fill={fill} {...base} />
        <circle cx={cx} cy={112} r={r * 0.42} fill={INK} />
        <circle cx={cx - r * 0.32} cy={112 - r * 0.32} r={r * 0.18} fill="#FFFFFF" />
      </g>
    );
  };

  // ---------- peinado ----------
  const fringe = (
    <path
      d="M46,86 C44,40 176,40 174,86 L162,90 L152,74 L140,90 L128,74 L116,90 L104,74 L92,90 L80,75 L66,90 L54,86 Z"
      fill={hairSwatch}
      stroke={INK}
      strokeWidth={stroke}
      strokeLinejoin="round"
    />
  );
  const sideLocks = (
    <g fill={hairSwatch} stroke={INK} strokeWidth={stroke}>
      <path d="M62,62 C84,38 136,38 158,62 C136,56 84,56 62,62 Z" strokeLinejoin="round" />
      <rect x="44" y="64" width="16" height="70" rx="9" />
      <rect x="160" y="64" width="16" height="70" rx="9" />
    </g>
  );
  const wavy = (
    <g fill={hairSwatch} stroke={INK} strokeWidth={stroke}>
      <path d="M46,74 C44,34 176,34 174,74 Z" strokeLinejoin="round" />
      <circle cx="76" cy="74" r="11" />
      <circle cx="110" cy="78" r="12" />
      <circle cx="144" cy="74" r="11" />
    </g>
  );
  const hair = hairCode === 'side_locks' ? sideLocks : hairCode === 'wavy' ? wavy : fringe;

  // ---------- ropa superior ----------
  const topFill = topCode === 'hoodie' ? '#7B61FF' : topCode === 'shirt' ? '#FFB997' : '#70D6C1';
  const torso = (
    <g>
      {topCode === 'hoodie' && (
        <path d="M70,164 C70,138 150,138 150,164 Z" fill="#6A4FE0" stroke={INK} strokeWidth={stroke} strokeLinejoin="round" />
      )}
      <rect x="46" y="166" width="128" height="92" rx="30" fill={topFill} stroke={INK} strokeWidth={stroke} />
      <circle cx="48" cy="190" r="15" fill={topFill} stroke={INK} strokeWidth={stroke} />
      <circle cx="172" cy="190" r="15" fill={topFill} stroke={INK} strokeWidth={stroke} />
      {topCode === 'tshirt' && (
        <path d="M110,196 l4.4,8.4 9.3,1.2 -6.9,6.4 1.8,9.2 -8.6,-4.7 -8.6,4.7 1.8,-9.2 -6.9,-6.4 9.3,-1.2 Z"
          fill="#FFE29A" stroke={INK} strokeWidth={2} strokeLinejoin="round" />
      )}
      {topCode === 'hoodie' && (
        <g stroke={INK} strokeWidth={2.5} strokeLinecap="round">
          <rect x="84" y="208" width="52" height="26" rx="9" fill="#6A4FE0" />
          <line x1="102" y1="172" x2="102" y2="190" />
          <line x1="118" y1="172" x2="118" y2="190" />
        </g>
      )}
      {topCode === 'shirt' && (
        <g stroke={INK} strokeWidth={2.5} strokeLinejoin="round">
          <path d="M110,166 L94,172 L110,190 Z" fill="#FFF6EA" />
          <path d="M110,166 L126,172 L110,190 Z" fill="#FFF6EA" />
          <circle cx="110" cy="202" r="2.4" fill={INK} stroke="none" />
          <circle cx="110" cy="214" r="2.4" fill={INK} stroke="none" />
        </g>
      )}
    </g>
  );

  // ---------- ropa inferior ----------
  const bottom =
    bottomCode === 'skirt' ? (
      <g>
        <rect x="64" y="256" width="26" height="44" rx="10" fill={fur} stroke={INK} strokeWidth={stroke} />
        <rect x="130" y="256" width="26" height="44" rx="10" fill={fur} stroke={INK} strokeWidth={stroke} />
        <path d="M56,238 L164,238 L184,286 Q110,304 36,286 Z" fill="#FF8FAB" stroke={INK} strokeWidth={stroke} strokeLinejoin="round" />
      </g>
    ) : bottomCode === 'pants' ? (
      <g fill="#2F9E8B" stroke={INK} strokeWidth={stroke}>
        <rect x="58" y="238" width="44" height="62" rx="15" />
        <rect x="118" y="238" width="44" height="62" rx="15" />
      </g>
    ) : (
      <g stroke={INK} strokeWidth={stroke}>
        <rect x="64" y="252" width="26" height="48" rx="10" fill={fur} />
        <rect x="130" y="252" width="26" height="48" rx="10" fill={fur} />
        <path d="M52,232 L168,232 L168,266 L120,266 L110,244 L100,266 L52,266 Z" fill="#E45555" strokeLinejoin="round" />
      </g>
    );

  // ---------- accesorio ----------
  const accessory =
    accessoryCode === 'glasses' ? (
      <g stroke={INK} strokeWidth={4.5} fill="#FFFFFF" fillOpacity={0.12}>
        <circle cx="82" cy="112" r="16.5" />
        <circle cx="138" cy="112" r="16.5" />
        <line x1="98.5" y1="112" x2="121.5" y2="112" />
        <line x1="65.5" y1="110" x2="46" y2="104" />
        <line x1="154.5" y1="110" x2="174" y2="104" />
      </g>
    ) : accessoryCode === 'bow' ? (
      <g transform="translate(110 178)" fill="#D64545" stroke={INK} strokeWidth={stroke} strokeLinejoin="round">
        <path d="M0,0 L-26,-13 L-26,13 Z" />
        <path d="M0,0 L26,-13 L26,13 Z" />
        <rect x="-7.5" y="-7.5" width="15" height="15" rx="4" />
      </g>
    ) : accessoryCode === 'beanie' ? (
      <g stroke={INK} strokeWidth={stroke} strokeLinejoin="round">
        <path d="M50,66 C50,20 170,20 170,66 Z" fill="#FFD166" />
        <path d="M56,48 C96,36 124,36 164,48" fill="none" stroke="#E45555" strokeWidth={5} strokeLinecap="round" />
        <circle cx="110" cy="14" r="9.5" fill="#FFF3DF" />
      </g>
    ) : null;

  return (
    <svg
      viewBox="0 0 220 300"
      width={size}
      height={height}
      className={className}
      role="img"
      aria-label="Gato chibi"
    >
      {/* ropa inferior */}
      {bottom}
      {/* torso */}
      {torso}
      {/* orejas */}
      <path d="M52,66 L28,16 L88,34 Z" fill={fur} stroke={INK} strokeWidth={stroke} strokeLinejoin="round" />
      <path d="M168,66 L192,16 L132,34 Z" fill={fur} stroke={INK} strokeWidth={stroke} strokeLinejoin="round" />
      <path d="M52,52 L38,26 L74,38 Z" fill={innerEar} />
      <path d="M168,52 L182,26 L146,38 Z" fill={innerEar} />
      {/* cabeza */}
      <ellipse cx="110" cy="112" rx="74" ry="57" fill={fur} stroke={INK} strokeWidth={stroke} />
      {bicolorPatch}
      {tabbyStripes}
      {darkSpots}
      {/* mejilla clara */}
      <ellipse cx="110" cy="136" rx="34" ry="17" fill={muzzle} opacity={0.9} />
      {/* peinado */}
      {hair}
      {/* cara */}
      {eye(82, 1)}
      {eye(138, -1)}
      <path d="M101,131 L119,131 L110,141 Z" fill="#FF6B6B" stroke={INK} strokeWidth={2.4} strokeLinejoin="round" />
      <path d="M110,141 L110,147 M110,147 Q101,156 90,151 M110,147 Q119,156 130,151"
        fill="none" stroke={INK} strokeWidth={2.4} strokeLinecap="round" />
      <ellipse cx="64" cy="144" rx="7" ry="4.4" fill="#FF9D9D" opacity={0.75} />
      <ellipse cx="156" cy="144" rx="7" ry="4.4" fill="#FF9D9D" opacity={0.75} />
      <g stroke={INK} strokeWidth={2} strokeLinecap="round" opacity={0.45}>
        <line x1="34" y1="128" x2="68" y2="132" />
        <line x1="34" y1="140" x2="68" y2="140" />
        <line x1="34" y1="152" x2="68" y2="148" />
        <line x1="186" y1="128" x2="152" y2="132" />
        <line x1="186" y1="140" x2="152" y2="140" />
        <line x1="186" y1="152" x2="152" y2="148" />
      </g>
      {/* accesorio */}
      {accessory}
    </svg>
  );
}
