import type { TicketSource } from '../types/ticket'

export const SOURCE_LABELS: Record<TicketSource, string> = {
  manual: 'Ręczne',
  csv: 'CSV',
}

const COLOR: Record<TicketSource, string> = {
  manual: 'bg-gray-700/60 text-gray-400 border-gray-600',
  csv: 'bg-purple-500/15 text-purple-300 border-purple-500/30',
}

export default function SourceBadge({ source }: { source: TicketSource }) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${COLOR[source] ?? 'bg-gray-700 text-gray-300 border-gray-600'}`}>
      {SOURCE_LABELS[source] ?? source}
    </span>
  )
}
