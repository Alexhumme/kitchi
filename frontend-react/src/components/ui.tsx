// Piezas compartidas de la interfaz: toasts, diálogos, estados vacíos y títulos.
import { useEffect, type ReactNode } from 'react';
import { AnimatePresence, motion } from 'framer-motion';
import { Check, Info, OctagonX, TriangleExclamationPoint } from 'lucide-react';
import { useKitchi } from '../state/AppContext';
import type { Toast } from '../state/AppContext';

const TONE_ICON: Record<Toast['tone'], ReactNode> = {
  info: <Info size={13} strokeWidth={3} />,
  success: <Check size={13} strokeWidth={3} />,
  error: <OctagonX size={13} strokeWidth={3} />,
  warn: <TriangleExclamationPoint size={13} strokeWidth={3} />,
};

export function ToastViewport() {
  const { toasts, dismissToast } = useKitchi();
  return (
    <div className="absolute left-0 right-0 top-3 z-50 flex flex-col items-center gap-2 px-6" aria-live="polite">
      <AnimatePresence>
        {toasts.map((toast) => (
          <motion.div
            key={toast.id}
            layout
            initial={{ opacity: 0, y: -18, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -12, scale: 0.95 }}
            transition={{ type: 'spring', stiffness: 500, damping: 32 }}
            className={`toast toast--${toast.tone}`}
            role="status"
            onClick={() => dismissToast(toast.id)}
          >
            <span className="toast__icon" aria-hidden="true">{TONE_ICON[toast.tone]}</span>
            <span className="toast__text">{toast.text}</span>
          </motion.div>
        ))}
      </AnimatePresence>
    </div>
  );
}

export function ConfirmDialog({
  open,
  title,
  body,
  confirmLabel,
  danger,
  onConfirm,
  onCancel,
}: {
  open: boolean;
  title: string;
  body: string;
  confirmLabel: string;
  danger?: boolean;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  useEffect(() => {
    if (!open) return undefined;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onCancel();
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, [open, onCancel]);

  if (!open) return null;
  return (
    <div className="absolute inset-0 z-40 flex items-center justify-center bg-black/45 p-6 backdrop-blur-[2px]"
      role="alertdialog" aria-modal="true" aria-label={title}>
      <motion.div
        initial={{ opacity: 0, scale: 0.85, y: 30 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ type: 'spring', stiffness: 480, damping: 30 }}
        className="bevel-panel w-full max-w-sm p-5"
      >
        <h2 className="text-lg font-extrabold text-[var(--ink)]">{title}</h2>
        <p className="mt-2 text-[0.95rem] font-medium text-[var(--ink-soft)]">{body}</p>
        <div className="mt-5 flex justify-end gap-2">
          <button type="button" className="bevel-btn px-4 py-2 text-sm font-extrabold" onClick={onCancel}>
            Cancelar
          </button>
          <button
            type="button"
            className={danger ? 'bevel-btn-coral px-4 py-2 text-sm' : 'bevel-btn-yellow px-4 py-2 text-sm'}
            onClick={onConfirm}
            autoFocus
          >
            {confirmLabel}
          </button>
        </div>
      </motion.div>
    </div>
  );
}

export function EmptyState({ icon, title, body, action }: {
  icon: ReactNode;
  title: string;
  body: string;
  action?: ReactNode;
}) {
  return (
    <div className="flex flex-col items-center justify-center gap-3 rounded-[var(--radio-grande)] px-6 py-10 text-center">
      <div className="grid h-16 w-16 place-items-center rounded-[var(--radio-grande)] bg-[var(--crema-hondo)] text-[var(--ink)] shadow-[inset_-4px_-5px_0_0_var(--ink)]" aria-hidden="true">{icon}</div>
      <h3 className="text-lg font-extrabold text-[var(--ink)]">{title}</h3>
      <p className="max-w-xs text-sm font-medium leading-snug text-[var(--tinta-suave)]">{body}</p>
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}

export function SectionTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="mb-1 shrink-0">
      <h1 className="inline-block rounded-xl bg-[var(--superficie)]/75 px-1.5 text-[1.55rem] font-extrabold leading-tight text-[var(--ink)] backdrop-blur-[1px]">{title}</h1>
      {subtitle && (
        <p className="mt-1 inline-block rounded-full bg-[var(--superficie)]/85 px-2.5 py-0.5 text-[0.78rem] font-bold text-[var(--ink-soft)] backdrop-blur-[1px]">
          {subtitle}
        </p>
      )}
    </div>
  );
}

export function Toggle({ checked, onChange, label }: { checked: boolean; onChange: (v: boolean) => void; label: string }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label={label}
      className="bevel-toggle"
      data-checked={checked}
      onClick={() => onChange(!checked)}
    >
      <span className="bevel-toggle__thumb" />
    </button>
  );
}
