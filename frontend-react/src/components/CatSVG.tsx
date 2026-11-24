// Gato compuesto con los assets reales de la diseñadora.
// Orden: cabello atrás → cuerpo → inferior → superior → cabeza → cabello delante → accesorios.
import { normalizeConfiguration } from '../lib/catalog';
import {
  BASE_ANCHOR,
  BOTTOM_ANCHOR,
  HAIR_BACK_ANCHOR,
  HAIR_FRONT_ANCHOR,
  HEAD_ANCHOR,
  TOP_ANCHOR,
  accessoryByCode,
  baseAsset,
  bottomByCode,
  colorize,
  colorizeBase,
  getAsset,
  hairByCode,
  headAsset,
  placeTransform,
  topByCode,
} from '../lib/characters';

const VIEWBOX = '0 -10 206.068 270';

interface Props {
  configuration: unknown;
  size?: number;
  className?: string;
}

function Layer({ inner, transform }: { inner: string; transform: string }) {
  return <g transform={transform} dangerouslySetInnerHTML={{ __html: inner }} />;
}

export default function CatSVG({ configuration, size = 200, className }: Props) {
  const cfg = normalizeConfiguration(configuration);
  const hair = hairByCode(cfg.hair.code);
  const top = topByCode(cfg.top.code);
  const bottom = bottomByCode(cfg.bottom.code);

  const base = baseAsset();
  const head = headAsset();
  const backHair = getAsset(hair.back);
  const frontHair = getAsset(hair.front);
  const topAsset = getAsset(top.file);
  const bottomAsset = getAsset(bottom.file);
  const furBase = cfg.fur.base_color ?? '#F2A15A';
  const eyeColor = cfg.eyes.color ?? '#211B26';

  return (
    <svg
      className={className}
      width={size}
      height={(size * 270) / 206.068}
      viewBox={VIEWBOX}
      role="img"
      aria-label="Gato personalizado"
      xmlns="http://www.w3.org/2000/svg"
    >
      <Layer inner={colorize(backHair, cfg.hair.color ?? '#6B4226')} transform={placeTransform(backHair, HAIR_BACK_ANCHOR)} />
      <Layer inner={colorizeBase(base, furBase, eyeColor)} transform={placeTransform(base, BASE_ANCHOR)} />
      <Layer inner={colorize(bottomAsset, cfg.bottom.color ?? '#FCFCFC')} transform={placeTransform(bottomAsset, BOTTOM_ANCHOR)} />
      <Layer inner={colorize(topAsset, cfg.top.color ?? '#FCFCFC')} transform={placeTransform(topAsset, TOP_ANCHOR)} />
      <Layer inner={colorizeBase(head, furBase, eyeColor)} transform={placeTransform(head, HEAD_ANCHOR)} />
      <Layer inner={colorize(frontHair, cfg.hair.color ?? '#6B4226')} transform={placeTransform(frontHair, HAIR_FRONT_ANCHOR)} />
      {cfg.accessories.map((entry) => {
        const accessory = accessoryByCode(entry.code);
        const asset = getAsset(accessory.file);
        return (
          <Layer
            key={entry.code}
            inner={colorize(asset, entry.color ?? accessory.color)}
            transform={placeTransform(asset, accessory.anchor)}
          />
        );
      })}
    </svg>
  );
}
