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
              ? 'px-4 py-2 rounded-lg bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium transition-colors'
              : 'px-4 py-2 rounded-lg border border-gray-700 hover:border-violet-500/60 hover:bg-gray-800/60 text-gray-300 hover:text-gray-100 text-sm font-medium transition-colors'
          }
        >
          {action.label}
        </Link>
      ))}
    </div>
  )
}
