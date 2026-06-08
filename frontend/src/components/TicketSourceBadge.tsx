import type { TicketSource } from '../types/ticket'

const LABELS: Record<TicketSource, string> = {
  manual: 'Ręczne',
  csv: 'CSV',
}

interface Props {
  source: TicketSource
}

export default function TicketSourceBadge({ source }: Props) {
  return (
    <span className="badge badge--source">
      {LABELS[source] ?? source}
    </span>
  )
}
