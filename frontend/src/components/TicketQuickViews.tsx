import type { Ticket, TicketStatus } from '../types/ticket'

export type QuickView = TicketStatus | 'email' | 'all'

interface QuickViewDef {
  id: QuickView
  label: string
}

const VIEWS: QuickViewDef[] = [
  { id: 'all', label: 'Wszystkie' },
  { id: 'open', label: 'Otwarte' },
  { id: 'ai_reviewed', label: 'Zweryfikowane przez AI' },
  { id: 'pending', label: 'Oczekujące' },
  { id: 'resolved', label: 'Rozwiązane' },
  { id: 'email', label: 'Z e-maila' },
]

interface Props {
  active: QuickView
  counts: Partial<Record<QuickView, number>>
  onChange: (view: QuickView) => void
}

export function applyQuickView(tickets: Ticket[], view: QuickView): Ticket[] {
  if (view === 'all') return tickets
  if (view === 'email') return tickets.filter(t => t.source === 'email')
  return tickets.filter(t => t.status === view)
}

export default function TicketQuickViews({ active, counts, onChange }: Props) {
  return (
    <div className="flex flex-wrap gap-2">
      {VIEWS.map(v => {
        const isActive = active === v.id
        const count = counts[v.id]
        return (
          <button
            key={v.id}
            onClick={() => onChange(v.id)}
            className={[
              'px-3 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap',
              isActive
                ? 'bg-violet-600 text-white'
                : 'bg-gray-800/60 border border-gray-700 text-gray-400 hover:text-gray-200 hover:border-gray-600',
            ].join(' ')}
          >
            {v.label}
            {count !== undefined && (
              <span className={`ml-1.5 text-xs px-1.5 py-0.5 rounded-full ${isActive ? 'bg-white/20' : 'bg-gray-700 text-gray-400'}`}>
                {count}
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
