export type TimelineIconType =
  | 'ticket'
  | 'email'
  | 'open'
  | 'ai'
  | 'category'
  | 'priority'
  | 'ai-response'
  | 'feedback'
  | 'agent'
  | 'resolved'

export interface TimelineEvent {
  id: string
  label: string
  sublabel?: string
  date: Date
  iconType: TimelineIconType
}

const ICON_STYLES: Record<TimelineIconType, { bg: string; border: string; text: string }> = {
  ticket:      { bg: 'bg-violet-500/20', border: 'border-violet-500/50', text: 'text-violet-300' },
  email:       { bg: 'bg-cyan-500/20',   border: 'border-cyan-500/50',   text: 'text-cyan-300'   },
  open:        { bg: 'bg-gray-700/50',   border: 'border-gray-600',      text: 'text-gray-400'   },
  ai:          { bg: 'bg-blue-500/20',   border: 'border-blue-500/50',   text: 'text-blue-300'   },
  category:    { bg: 'bg-indigo-500/20', border: 'border-indigo-500/50', text: 'text-indigo-300' },
  priority:    { bg: 'bg-orange-500/20', border: 'border-orange-500/50', text: 'text-orange-300' },
  'ai-response': { bg: 'bg-blue-500/20', border: 'border-blue-500/50',  text: 'text-blue-300'   },
  feedback:    { bg: 'bg-yellow-500/20', border: 'border-yellow-500/50', text: 'text-yellow-300' },
  agent:       { bg: 'bg-green-500/20',  border: 'border-green-500/50',  text: 'text-green-300'  },
  resolved:    { bg: 'bg-green-500/20',  border: 'border-green-500/50',  text: 'text-green-300'  },
}

const ICONS: Record<TimelineIconType, React.ReactNode> = {
  ticket: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <path d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2"/>
      <rect x="9" y="3" width="6" height="4" rx="1"/>
    </svg>
  ),
  email: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
      <polyline points="22,6 12,13 2,6"/>
    </svg>
  ),
  open: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <circle cx="12" cy="12" r="9"/>
      <line x1="12" y1="8" x2="12" y2="12"/>
      <line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
  ),
  ai: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <circle cx="12" cy="12" r="3"/>
      <path d="M12 2v3M12 19v3M2 12h3M19 12h3"/>
    </svg>
  ),
  category: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <path d="M4 6h16M4 12h16M4 18h7"/>
    </svg>
  ),
  priority: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <polyline points="18 15 12 9 6 15"/>
    </svg>
  ),
  'ai-response': (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/>
    </svg>
  ),
  feedback: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
    </svg>
  ),
  agent: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
      <circle cx="12" cy="7" r="4"/>
    </svg>
  ),
  resolved: (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3">
      <polyline points="20 6 9 17 4 12"/>
    </svg>
  ),
}

function formatDate(date: Date) {
  return date.toLocaleString('pl-PL', { dateStyle: 'short', timeStyle: 'short' })
}

interface Props {
  event: TimelineEvent
  isLast: boolean
}

export default function TimelineItem({ event, isLast }: Props) {
  const style = ICON_STYLES[event.iconType]

  return (
    <div className="flex gap-3">
      {/* Left: dot + connector line */}
      <div className="flex flex-col items-center flex-shrink-0">
        <div className={`w-6 h-6 rounded-full border flex items-center justify-center ${style.bg} ${style.border} ${style.text}`}>
          {ICONS[event.iconType]}
        </div>
        {!isLast && (
          <div className="w-px flex-1 min-h-[16px] bg-white/8 mt-1" />
        )}
      </div>

      {/* Right: content */}
      <div className={`pb-4 min-w-0 flex-1 ${isLast ? '' : ''}`}>
        <p className="text-sm text-gray-200 leading-snug">{event.label}</p>
        {event.sublabel && (
          <p className="text-xs text-gray-500 mt-0.5 leading-snug">{event.sublabel}</p>
        )}
        <p className="text-xs text-gray-600 mt-1">{formatDate(event.date)}</p>
      </div>
    </div>
  )
}
