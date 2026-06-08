import { createContext, useCallback, useContext, useRef, useState } from 'react'

export type ToastVariant = 'info' | 'success' | 'warning' | 'error'

export interface Toast {
  id: number
  message: string
  variant: ToastVariant
  onClick?: () => void
}

interface ToastContextValue {
  showToast: (message: string, variant?: ToastVariant, onClick?: () => void) => void
}

export const ToastContext = createContext<ToastContextValue>({
  showToast: () => {},
})

export function useToast() {
  return useContext(ToastContext)
}

const VARIANTS: Record<ToastVariant, { bg: string; border: string; icon: string; text: string }> = {
  info:    { bg: 'bg-[#1a1d27]', border: 'border-blue-500/40',  icon: 'text-blue-400',  text: 'text-gray-200' },
  success: { bg: 'bg-[#1a1d27]', border: 'border-green-500/40', icon: 'text-green-400', text: 'text-gray-200' },
  warning: { bg: 'bg-[#1a1d27]', border: 'border-amber-500/40', icon: 'text-amber-400', text: 'text-gray-200' },
  error:   { bg: 'bg-[#1a1d27]', border: 'border-red-500/40',   icon: 'text-red-400',   text: 'text-gray-200' },
}

const ICONS: Record<ToastVariant, JSX.Element> = {
  info: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-5 h-5">
      <circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>
    </svg>
  ),
  success: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-5 h-5">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
  warning: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-5 h-5">
      <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
      <line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>
    </svg>
  ),
  error: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-5 h-5">
      <circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/>
    </svg>
  ),
}

let _nextId = 1

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([])
  const timers = useRef<Map<number, ReturnType<typeof setTimeout>>>(new Map())

  const dismiss = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
    const t = timers.current.get(id)
    if (t) { clearTimeout(t); timers.current.delete(id) }
  }, [])

  const showToast = useCallback(
    (message: string, variant: ToastVariant = 'info', onClick?: () => void) => {
      const id = _nextId++
      setToasts((prev) => [...prev.slice(-4), { id, message, variant, onClick }])
      const timer = setTimeout(() => dismiss(id), 6000)
      timers.current.set(id, timer)
    },
    [dismiss],
  )

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {/* Toast container — top-center, below the fixed header */}
      <div className="pointer-events-none fixed left-1/2 top-20 z-50 flex w-[min(calc(100vw-2rem),34rem)] -translate-x-1/2 flex-col gap-2 items-center">
        {toasts.map((toast) => {
          const v = VARIANTS[toast.variant]
          return (
            <div
              key={toast.id}
              className={[
                'pointer-events-auto flex w-full items-start gap-3 rounded-full border px-4 py-3 shadow-xl backdrop-blur-xl',
                'transition-all duration-300',
                v.bg, v.border,
                toast.onClick ? 'cursor-pointer hover:brightness-110 active:scale-[0.98]' : '',
              ].join(' ')}
              role="alert"
              onClick={() => {
                if (toast.onClick) { toast.onClick(); dismiss(toast.id) }
              }}
            >
              <span className={`mt-0.5 shrink-0 ${v.icon}`}>{ICONS[toast.variant]}</span>
              <div className="flex-1 min-w-0">
                <p className={`text-sm leading-snug ${v.text}`}>{toast.message}</p>
                {toast.onClick && (
                  <p className="text-xs text-gray-500 mt-0.5">Kliknij, aby odświeżyć</p>
                )}
              </div>
              <button
                className="text-gray-600 hover:text-gray-300 transition-colors ml-1 shrink-0"
                onClick={(e) => { e.stopPropagation(); dismiss(toast.id) }}
                aria-label="Zamknij"
              >
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
                  <line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>
                </svg>
              </button>
            </div>
          )
        })}
      </div>
    </ToastContext.Provider>
  )
}
