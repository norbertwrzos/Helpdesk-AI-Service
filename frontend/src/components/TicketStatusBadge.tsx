import type { TicketStatus } from '../types/ticket'
import { TICKET_STATUS_LABELS } from '../types/ticket'

const COLOR_CLASS: Record<TicketStatus, string> = {
  open: 'badge--open',
  ai_reviewed: 'badge--ai-reviewed',
  pending: 'badge--pending',
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
