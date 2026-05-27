import { Link } from 'react-router-dom'
import type { Ticket } from '../types/ticket'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import TicketStatusBadge from './TicketStatusBadge'
import TicketSourceBadge from './TicketSourceBadge'

interface Props {
  tickets: Ticket[]
  categories: Category[]
  priorities: Priority[]
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('pl-PL', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}

export default function TicketList({ tickets, categories, priorities }: Props) {
  const categoryMap = Object.fromEntries(categories.map(c => [c.id, c.name]))
  const priorityMap = Object.fromEntries(priorities.map(p => [p.id, p.name]))

  const sorted = [...tickets].sort(
    (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
  )

  if (sorted.length === 0) {
    return (
      <div className="empty-state">
        <span className="empty-state__icon">📭</span>
        <p>Brak zgłoszeń. Dodaj pierwsze zgłoszenie za pomocą formularza powyżej.</p>
      </div>
    )
  }

  return (
    <div className="ticket-list">
      {sorted.map(ticket => (
        <div key={ticket.id} className="ticket-card">
          <div className="ticket-card__header">
            <span className="ticket-card__id">#{ticket.id}</span>
            <div className="ticket-card__badges">
              <TicketStatusBadge status={ticket.status} />
              <TicketSourceBadge source={ticket.source} />
            </div>
          </div>

          <h3 className="ticket-card__title">{ticket.title}</h3>

          <div className="ticket-card__meta">
            {ticket.category_id && (
              <span className="ticket-card__meta-item">
                📂 {categoryMap[ticket.category_id] ?? `Kat. #${ticket.category_id}`}
              </span>
            )}
            {ticket.priority_id && (
              <span className="ticket-card__meta-item">
                🚦 {priorityMap[ticket.priority_id] ?? `Priorytet #${ticket.priority_id}`}
              </span>
            )}
            <span className="ticket-card__meta-item">🕐 {formatDate(ticket.created_at)}</span>
          </div>

          <Link to={`/tickets/${ticket.id}`} className="btn btn--secondary btn--sm">
            Szczegóły →
          </Link>
        </div>
      ))}
    </div>
  )
}
