import type { TicketStatus } from '../types/ticket'

const LABELS: Record<TicketStatus, string> = {
  new: 'Nowe',
  in_analysis: 'W analizie',
  answered: 'Odpowiedziane',
  resolved: 'Rozwiązane',
  rejected: 'Odrzucone',
}

const COLOR_CLASS: Record<TicketStatus, string> = {
  new: 'badge--new',
  in_analysis: 'badge--in-analysis',
  answered: 'badge--answered',
  resolved: 'badge--resolved',
  rejected: 'badge--rejected',
}

interface Props {
  status: TicketStatus
}

export default function TicketStatusBadge({ status }: Props) {
  return (
    <span className={`badge ${COLOR_CLASS[status]}`}>
      {LABELS[status] ?? status}
    </span>
  )
}
