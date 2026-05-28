import type { TicketStatus } from '../types/ticket'
import { TICKET_STATUS_LABELS } from '../types/ticket'

const COLOR: Record<TicketStatus, string> = {
  open: 'bg-violet-500/15 text-violet-300 border-violet-500/30',
  ai_reviewed: 'bg-blue-500/15 text-blue-300 border-blue-500/30',
  pending: 'bg-yellow-500/15 text-yellow-300 border-yellow-500/30',
  resolved: 'bg-green-500/15 text-green-300 border-green-500/30',
  rejected: 'bg-red-500/15 text-red-300 border-red-500/30',
}

export default function StatusBadge({ status }: { status: TicketStatus }) {
  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-md text-xs font-medium border ${COLOR[status] ?? 'bg-gray-700 text-gray-300 border-gray-600'}`}>
      {TICKET_STATUS_LABELS[status] ?? status}
    </span>
  )
}
