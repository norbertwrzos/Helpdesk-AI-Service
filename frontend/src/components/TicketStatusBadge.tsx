import type { TicketStatus } from '../types/ticket'
import { TICKET_STATUS_LABELS } from '../types/ticket'

const COLOR_CLASS: Record<TicketStatus, string> = {
  open: 'badge--new',
  ai_reviewed: 'badge--in-analysis',
  pending: 'badge--answered',
  resolved: 'badge--resolved',
  rejected: 'badge--rejected',
}

interface Props {
  status: TicketStatus
}

export default function TicketStatusBadge({ status }: Props) {
  return (
    <span className={`badge ${COLOR_CLASS[status]}`}>
      {TICKET_STATUS_LABELS[status] ?? status}
    </span>
  )
}
