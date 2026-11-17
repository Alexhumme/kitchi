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
    <div className="toast-viewport" aria-live="polite">
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
    <div className="confirm-overlay" role="alertdialog" aria-modal="true" aria-label={title}>
      <motion.div
        initial={{ opacity: 0, scale: 0.85, y: 30 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ type: 'spring', stiffness: 480, damping: 30 }}
        className="bevel-panel confirm-panel"
      >
        <h2 className="confirm-title">{title}</h2>
        <p className="confirm-body">{body}</p>
        <div className="confirm-actions">
          <button type="button" className="bevel-btn" onClick={onCancel}>
            Cancelar
          </button>
          <button
            type="button"
            className={danger ? 'bevel-btn-coral' : 'bevel-btn-yellow'}
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
    <div className="empty-state">
      <div className="empty-state__icon" aria-hidden="true">{icon}</div>
      <h3 className="empty-state__title">{title}</h3>
      <p className="empty-state__body">{body}</p>
      {action && <div className="empty-state__action">{action}</div>}
    </div>
  );
}

export function SectionTitle({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="section-title">
      <h1 className="section-title__heading">{title}</h1>
      {subtitle && <p className="section-title__subtitle">{subtitle}</p>}
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
