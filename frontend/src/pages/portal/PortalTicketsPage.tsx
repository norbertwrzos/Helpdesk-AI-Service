import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getTickets } from '../../api/tickets'
import { getCategories } from '../../api/categories'
import { getPriorities } from '../../api/priorities'
import type { Ticket } from '../../types/ticket'
import type { Category } from '../../types/category'
import type { Priority } from '../../types/priority'
import TicketForm from '../../components/TicketForm'
import LoadingState from '../../components/LoadingState'
import TicketStatusBadge from '../../components/TicketStatusBadge'
import { useAuth } from '../../auth/AuthContext'

export default function PortalTicketsPage() {
  const { currentUser } = useAuth()
  const navigate = useNavigate()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [priorities, setPriorities] = useState<Priority[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [showForm, setShowForm] = useState(false)

  async function loadAll() {
    setError(null)
    try {
      const [t, c, p] = await Promise.all([getTickets(), getCategories(), getPriorities()])
      // Filter to only show tickets belonging to current user
      const myTickets = t.filter(
        (ticket) =>
          !ticket.requester_email ||
          ticket.requester_email.toLowerCase() === currentUser?.email.toLowerCase(),
      )
      setTickets(myTickets)
      setCategories(c)
      setPriorities(p)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd połączenia z serwerem.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadAll()
  }, [])

  const categoryMap = Object.fromEntries(categories.map((c) => [c.id, c.name]))
  const priorityMap = Object.fromEntries(priorities.map((p) => [p.id, p.name]))

  return (
    <div className="page">
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="page__title">Moje zgłoszenia</h1>
          <p className="page__subtitle">Historia Twoich zgłoszeń technicznych.</p>
        </div>
        <button
          onClick={() => setShowForm((v) => !v)}
          className="flex items-center gap-2 bg-violet-600 hover:bg-violet-700 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} className="w-4 h-4">
            <line x1="12" y1="5" x2="12" y2="19" />
            <line x1="5" y1="12" x2="19" y2="12" />
          </svg>
          {showForm ? 'Anuluj' : 'Nowe zgłoszenie'}
        </button>
      </div>

      {showForm && (
        <div className="mb-6">
          <TicketForm
            categories={categories}
            priorities={priorities}
            defaultRequesterEmail={currentUser?.email}
            onSuccess={() => {
              setShowForm(false)
              loadAll()
            }}
          />
        </div>
      )}

      {loading && <LoadingState label="Pobieranie zgłoszeń…" />}
      {error && <div className="alert alert--error">{error}</div>}

      {!loading && !error && tickets.length === 0 && (
        <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-8 text-center">
          <p className="text-gray-500 text-sm">Nie masz jeszcze żadnych zgłoszeń.</p>
          <button
            onClick={() => setShowForm(true)}
            className="mt-3 text-violet-400 text-sm hover:underline"
          >
            Dodaj pierwsze zgłoszenie
          </button>
        </div>
      )}

      {!loading && !error && tickets.length > 0 && (
        <div className="space-y-2">
          {tickets.map((ticket) => (
            <div
              key={ticket.id}
              onClick={() => navigate(`/portal/tickets/${ticket.id}`)}
              className="flex items-center justify-between p-4 rounded-xl border border-gray-800 bg-gray-900/60 hover:bg-gray-800/60 cursor-pointer transition-colors"
            >
              <div className="min-w-0">
                <div className="text-sm font-medium text-gray-200 truncate">{ticket.title}</div>
                <div className="text-xs text-gray-600 mt-0.5">
                  {categoryMap[ticket.category_id ?? ''] ?? '—'} ·{' '}
                  {priorityMap[ticket.priority_id ?? ''] ?? '—'}
                </div>
              </div>
              <div className="flex items-center gap-3 flex-shrink-0 ml-4">
                <TicketStatusBadge status={ticket.status} />
                <span className="text-xs text-gray-600">
                  {new Date(ticket.created_at).toLocaleDateString('pl-PL')}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
