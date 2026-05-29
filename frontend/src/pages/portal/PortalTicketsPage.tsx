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
      const mine = all.filter(
        t => !t.requester_email ||
          t.requester_email.toLowerCase() === currentUser?.email.toLowerCase(),
      )
      setTickets(mine)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd połączenia z serwerem.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTickets()
  }, [])

  return (
    <PortalLayout>
      <div className="page space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between gap-4">
          <div>
            <h1 className="text-xl font-semibold text-gray-100">Moje zgłoszenia</h1>
            <p className="text-sm text-gray-500 mt-0.5">Historia Twoich zgłoszeń technicznych.</p>
          </div>
          <button
            onClick={() => setModalOpen(true)}
            className="flex items-center gap-2 bg-violet-600 hover:bg-violet-500 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors whitespace-nowrap"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} className="w-4 h-4">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            Nowe zgłoszenie
          </button>
        </div>

        {loading && <LoadingState label="Pobieranie zgłoszeń…" />}

        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl px-5 py-4 text-sm text-red-400">
            {error}
          </div>
        )}

        {!loading && !error && tickets.length === 0 && (
          <div className="bg-surface rounded-xl border border-white/8 p-10 text-center space-y-3">
            <p className="text-gray-500 text-sm">Nie masz jeszcze żadnych zgłoszeń.</p>
            <button
              onClick={() => setModalOpen(true)}
              className="text-violet-400 text-sm hover:text-violet-300 transition-colors"
            >
              Dodaj pierwsze zgłoszenie →
            </button>
          </div>
        )}

        {!loading && !error && tickets.length > 0 && (
          <div className="space-y-2">
            {tickets.map(ticket => (
              <div
                key={ticket.id}
                onClick={() => navigate(`/portal/tickets/${ticket.id}`)}
                className="flex items-center justify-between gap-4 p-4 rounded-xl border border-white/8 bg-surface hover:bg-white/5 cursor-pointer transition-colors group"
              >
                <div className="min-w-0 flex-1">
                  <div className="flex items-center gap-2 mb-0.5">
                    <span className="text-xs font-mono text-gray-600">#{ticket.id}</span>
                    <span className="text-sm font-medium text-gray-200 truncate group-hover:text-white transition-colors">
                      {ticket.title}
                    </span>
                  </div>
                  <p className="text-xs text-gray-500 truncate">
                    {ticket.description.slice(0, 100)}{ticket.description.length > 100 ? '…' : ''}
                  </p>
                </div>
                <div className="flex items-center gap-3 flex-shrink-0">
                  <StatusBadge status={ticket.status} />
                  <span className="text-xs text-gray-600">
                    {new Date(ticket.created_at).toLocaleDateString('pl-PL')}
                  </span>
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4 text-gray-700 group-hover:text-gray-500 transition-colors">
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
