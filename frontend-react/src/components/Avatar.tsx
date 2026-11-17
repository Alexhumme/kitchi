import type { CSSProperties } from 'react';

const PALETTE = ['#FF6B6B', '#7B61FF', '#2F9E8B', '#E45555', '#B07A1E', '#4DAD72'];

function hash(s: string): number {
  let h = 2166136261;
  for (let i = 0; i < s.length; i += 1) {
    h ^= s.charCodeAt(i);
    h = (h * 16777619) >>> 0;
  }
  return h;
}

export default function Avatar({ name, size = 36 }: { name: string; size?: number }) {
  const initial = (name.trim()[0] ?? '?').toUpperCase();
  const color = PALETTE[hash(name) % PALETTE.length];
  const style: CSSProperties = {
    width: size,
    height: size,
    fontSize: Math.max(11, Math.floor(size * 0.44)),
    background: color,
  };
  return (
    <div className="avatar" style={style} aria-hidden="true">
      {initial}
    </div>
  );
}
