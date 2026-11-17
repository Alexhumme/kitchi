// Micro-efectos: sonido (Web Audio) y vibración (navigator.vibrate).
// Sustituye a los efectos que Flet 1.x no podía reproducir en web.
let soundEnabled = true;
let hapticsEnabled = true;

export function syncFx(flags: { sound: boolean; haptics: boolean }): void {
  soundEnabled = flags.sound;
  hapticsEnabled = flags.haptics;
}

let audioCtx: AudioContext | null = null;

function context(): AudioContext | null {
  if (typeof window === 'undefined') return null;
  try {
    audioCtx ??= new (window.AudioContext ?? (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
    return audioCtx;
  } catch {
    return null;
  }
}

export type PopKind = 'tap' | 'success' | 'error' | 'nav';

export function pop(kind: PopKind = 'tap'): void {
  if (!soundEnabled) return;
  const ctx = context();
  if (!ctx) return;
  const now = ctx.currentTime;
  const specs: Record<PopKind, Array<[number, number, number]>> = {
    tap: [[620, 0, 0.06]],
    nav: [[440, 0, 0.05], [660, 0.07, 0.05]],
    success: [[523, 0, 0.09], [784, 0.09, 0.12]],
    error: [[180, 0, 0.16]],
  };
  for (const [freq, delay, duration] of specs[kind]) {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'triangle';
    osc.frequency.setValueAtTime(freq, now + delay);
    gain.gain.setValueAtTime(0.0001, now + delay);
    gain.gain.exponentialRampToValueAtTime(0.12, now + delay + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + delay + duration);
    osc.connect(gain).connect(ctx.destination);
    osc.start(now + delay);
    osc.stop(now + delay + duration + 0.02);
  }
}

export function haptic(pattern: number | number[] = 12): void {
  if (!hapticsEnabled) return;
  try {
    navigator.vibrate?.(pattern);
  } catch {
    // sin vibración en este dispositivo
  }
}
