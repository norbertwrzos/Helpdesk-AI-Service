import { Link, useNavigate } from 'react-router-dom'
import type { Ticket } from '../types/ticket'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import StatusBadge from './StatusBadge'
import PriorityBadge from './PriorityBadge'
import SourceBadge from './SourceBadge'
import EmptyState from './EmptyState'

interface Props {
  tickets: Ticket[]
  categories: Category[]
  priorities: Priority[]
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString('pl-PL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
  })
}

export default function TicketsTable({ tickets, categories, priorities }: Props) {
  const navigate = useNavigate()
  const categoryMap = Object.fromEntries(categories.map(c => [c.id, c.name]))
  const priorityMap = Object.fromEntries(priorities.map(p => [p.id, p]))

  function openTicket(ticketId: number) {
    navigate(`/tickets/${ticketId}`)
  }

  function handleRowKeyDown(event: React.KeyboardEvent<HTMLTableRowElement>, ticketId: number) {
    if (event.key !== 'Enter' && event.key !== ' ') return
    event.preventDefault()
    openTicket(ticketId)
  }

  if (tickets.length === 0) {
    return <EmptyState />
  }

  return (
    <div className="overflow-x-auto rounded-xl border border-gray-800">
      <table className="w-full text-sm">
        <thead>
          <tr className="bg-gray-900/80 text-left border-b border-gray-800">
            {['ID', 'Tytuł', 'Status', 'Priorytet', 'Kategoria', 'Źródło', 'Agent', 'Utworzono', 'Aktualizacja', 'Akcje'].map(col => (
              <th
                key={col}
                className="px-3 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider whitespace-nowrap first:pl-4 last:pr-4"
              >
                {col}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-800/60">
          {tickets.map(ticket => {
            const priority = ticket.priority_id != null ? priorityMap[ticket.priority_id] : null
            const category = ticket.category_id != null ? categoryMap[ticket.category_id] : null

            return (
              <tr
                key={ticket.id}
                tabIndex={0}
                role="link"
                onClick={() => openTicket(ticket.id)}
                onKeyDown={(event) => handleRowKeyDown(event, ticket.id)}
                className="group cursor-pointer transition-colors hover:bg-gray-800/30 focus:outline-none focus:ring-1 focus:ring-inset focus:ring-violet-500/50"
              >
                <td className="px-3 py-3 pl-4 text-gray-500 font-mono text-xs whitespace-nowrap">
                  #{ticket.id}
                </td>

                <td className="px-3 py-3 max-w-xs">
                  <span className="text-gray-200 line-clamp-2 leading-snug">{ticket.title}</span>
                </td>

                <td className="px-3 py-3 whitespace-nowrap">
                  <StatusBadge status={ticket.status} />
                </td>

                <td className="px-3 py-3 whitespace-nowrap">
                  {priority ? (
                    <PriorityBadge name={priority.name} level={priority.level} />
                  ) : (
                    <span className="text-gray-600 text-xs">—</span>
                  )}
                </td>

                <td className="px-3 py-3 text-gray-400 whitespace-nowrap">
                  {category ?? <span className="text-gray-600">—</span>}
                </td>

                <td className="px-3 py-3 whitespace-nowrap">
                  <SourceBadge source={ticket.source} />
                </td>

                <td className="px-3 py-3 text-gray-400 whitespace-nowrap">
                  {ticket.assigned_agent_name ?? <span className="text-gray-600 text-xs">Nieprzypisane</span>}
                </td>

                <td className="px-3 py-3 text-gray-500 text-xs whitespace-nowrap">
                  {formatDate(ticket.created_at)}
                </td>

                <td className="px-3 py-3 text-gray-500 text-xs whitespace-nowrap">
                  {formatDate(ticket.updated_at)}
                </td>

                <td className="px-3 py-3 pr-4 whitespace-nowrap">
                  <div className="flex items-center gap-2">
                    <Link
                      to={`/tickets/${ticket.id}`}
                      onClick={(event) => event.stopPropagation()}
                      className="px-2.5 py-1 rounded-md text-xs font-medium border border-gray-700 text-gray-400 hover:border-gray-500 hover:text-gray-200 transition-colors"
                    >
                      Edytuj
                    </Link>
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
