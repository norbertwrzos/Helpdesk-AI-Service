import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getTickets } from '../../api/tickets'
import type { Ticket } from '../../types/ticket'
import LoadingState from '../../components/LoadingState'
import StatusBadge from '../../components/StatusBadge'
import NewTicketModal from '../../components/NewTicketModal'
import PortalLayout from '../../components/PortalLayout'
import { useAuth } from '../../auth/AuthContext'

export default function PortalTicketsPage() {
  const { currentUser } = useAuth()
  const navigate = useNavigate()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [modalOpen, setModalOpen] = useState(false)

  async function loadTickets() {
    setError(null)
    setLoading(true)
    try {
      const all = await getTickets()
      const currentEmail = currentUser?.email.toLowerCase()
      const mine = all.filter(
        (ticket) => !ticket.requester_email || ticket.requester_email.toLowerCase() === currentEmail,
      )
      setTickets(mine)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd połączenia z serwerem.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    void loadTickets()
  }, [currentUser?.email])

  return (
    <PortalLayout>
      <div className="page">
        <div className="page__header">
          <div>
            <h1 className="page__title">Moje zgłoszenia</h1>
            <p className="page__subtitle">Historia Twoich zgłoszeń technicznych.</p>
          </div>
        </div>

        {loading && <LoadingState label="Pobieranie zgłoszeń…" />}

        {error && (
          <div className="rounded-2xl border border-red-500/20 bg-red-500/10 px-5 py-4 text-sm text-red-300">
            {error}
          </div>
        )}

        {!loading && !error && tickets.length === 0 && (
          <div className="surface-card surface-card--padded space-y-3 text-center">
            <p className="text-sm text-gray-500">Nie masz jeszcze żadnych zgłoszeń.</p>
            <button
              onClick={() => setModalOpen(true)}
              className="text-sm text-violet-400 transition-colors hover:text-violet-300"
            >
              Dodaj pierwsze zgłoszenie →
            </button>
          </div>
        )}

        {!loading && !error && tickets.length > 0 && (
          <div className="space-y-3">
            {tickets.map((ticket) => (
              <div
                key={ticket.id}
                onClick={() => navigate(`/portal/tickets/${ticket.id}`)}
                className="surface-card surface-card--interactive group flex cursor-pointer items-center justify-between gap-4 p-4"
              >
                <div className="min-w-0 flex-1">
                  <div className="mb-0.5 flex items-center gap-2">
                    <span className="text-xs font-mono text-gray-600">#{ticket.id}</span>
                    <span className="truncate text-sm font-medium text-gray-200 transition-colors group-hover:text-white">
                      {ticket.title}
                    </span>
                  </div>
                  <p className="truncate text-xs text-gray-500">
                    {ticket.description.slice(0, 100)}{ticket.description.length > 100 ? '…' : ''}
                  </p>
                </div>
                <div className="flex flex-shrink-0 items-center gap-3">
                  <StatusBadge status={ticket.status} />
                  <span className="text-xs text-gray-500">
                    {new Date(ticket.created_at).toLocaleDateString('pl-PL')}
                  </span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="h-4 w-4 text-gray-700 transition-colors group-hover:text-gray-500">
                    <polyline points="9 18 15 12 9 6" />
                  </svg>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <NewTicketModal isOpen={modalOpen} onClose={() => setModalOpen(false)} />
    </PortalLayout>
  )
}
