import { Link } from 'react-router-dom'
import type { Ticket } from '../types/ticket'
import TicketStatusBadge from './TicketStatusBadge'

interface Props {
  tickets: Ticket[]
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('pl-PL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

/**
 * Displays up to 5 most recent tickets in a compact table row format.
 */
export default function RecentTickets({ tickets }: Props) {
  if (tickets.length === 0) {
    return (
      <p className="text-sm text-gray-500 py-4 text-center">
        Brak zgłoszeń do wyświetlenia.
      </p>
    )
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-xs text-gray-500 uppercase tracking-wider border-b border-gray-800">
            <th className="pb-2 pr-4 font-medium">Tytuł</th>
            <th className="pb-2 pr-4 font-medium">Status</th>
            <th className="pb-2 pr-4 font-medium">Priorytet</th>
            <th className="pb-2 pr-4 font-medium">Data</th>
            <th className="pb-2 font-medium"></th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800/60">
          {tickets.map((ticket) => (
            <tr key={ticket.id} className="group hover:bg-gray-800/30 transition-colors">
              <td className="py-3 pr-4 text-gray-200 max-w-xs truncate">
                {ticket.title}
              </td>
              <td className="py-3 pr-4">
                <TicketStatusBadge status={ticket.status} />
              </td>
              <td className="py-3 pr-4 text-gray-400">
                {ticket.priority_id != null ? `#${ticket.priority_id}` : '—'}
              </td>
              <td className="py-3 pr-4 text-gray-500 whitespace-nowrap">
                {formatDate(ticket.created_at)}
              </td>
              <td className="py-3 text-right">
                <Link
                  to={`/tickets/${ticket.id}`}
                  className="text-violet-400 hover:text-violet-300 text-xs font-medium transition-colors"
                >
                  Szczegóły →
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
