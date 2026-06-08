import type { Ticket, TicketStatus } from '../types/ticket'

export type QuickView = TicketStatus | 'all'

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
]

interface Props {
  active: QuickView
  counts: Partial<Record<QuickView, number>>
  onChange: (view: QuickView) => void
}

const BUTTON_BASE = 'inline-flex items-center gap-2 whitespace-nowrap rounded-xl border px-3.5 py-2 text-sm font-medium transition-all'

export function applyQuickView(tickets: Ticket[], view: QuickView): Ticket[] {
  if (view === 'all') return tickets
  return tickets.filter(t => t.status === view)
}

export default function TicketQuickViews({ active, counts, onChange }: Props) {
  return (
    <div className="flex flex-wrap gap-2 rounded-2xl border border-white/10 bg-white/[0.02] p-2">
      {VIEWS.map(v => {
        const isActive = active === v.id
        const count = counts[v.id]
        return (
          <button
            key={v.id}
            onClick={() => onChange(v.id)}
            className={[
              BUTTON_BASE,
              isActive
                ? 'border-violet-300/20 bg-violet-500 text-white shadow-[0_10px_20px_rgba(99,102,241,0.22)]'
                : 'border-white/8 bg-white/[0.03] text-slate-300 hover:border-white/12 hover:bg-white/[0.05] hover:text-white',
            ].join(' ')}
          >
            {v.label}
            {count !== undefined && (
              <span
                className={[
                  'rounded-full px-1.5 py-0.5 text-xs font-semibold',
                  isActive ? 'bg-white/20 text-white' : 'bg-white/[0.06] text-slate-400',
                ].join(' ')}
              >
                {count}
              </span>
            )}
          </button>
        )
      })}
    </div>
  )
}
