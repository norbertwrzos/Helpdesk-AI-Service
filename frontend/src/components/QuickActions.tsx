import { Link } from 'react-router-dom'

interface Action {
  label: string
  to: string
  /** Tailwind classes for the button variant */
  variant?: 'primary' | 'secondary'
}

const ACTIONS: Action[] = [
  { label: 'Nowe zgłoszenie', to: '/tickets', variant: 'primary' },
  { label: 'Wszystkie zgłoszenia', to: '/tickets', variant: 'secondary' },
  { label: 'Baza wiedzy', to: '/knowledge', variant: 'secondary' },
]

/**
 * Quick-action shortcut buttons shown on the Dashboard.
 */
export default function QuickActions() {
  return (
    <div className="flex flex-wrap gap-3">
      {ACTIONS.map((action) => (
        <Link
          key={action.label}
          to={action.to}
          className={
            action.variant === 'primary'
              ? 'inline-flex items-center rounded-lg border border-violet-400/20 bg-violet-500 px-4 py-2 text-sm font-medium text-white shadow-[0_10px_22px_rgba(15,23,42,0.16)] transition-all hover:-translate-y-px hover:bg-violet-400'
              : 'inline-flex items-center rounded-lg border border-gray-700 bg-white/[0.02] px-4 py-2 text-sm font-medium text-gray-300 transition-colors hover:border-violet-500/40 hover:bg-gray-800/60 hover:text-gray-100'
          }
        >
          {action.label}
        </Link>
      ))}
    </div>
  )
}
