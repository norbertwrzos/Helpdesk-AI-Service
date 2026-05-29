import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getTicket } from '../../api/tickets'
import type { Ticket } from '../../types/ticket'
import LoadingState from '../../components/LoadingState'
import StatusBadge from '../../components/StatusBadge'
import SourceBadge from '../../components/SourceBadge'
import AIResponseHistory from '../../components/AIResponseHistory'
import PortalLayout from '../../components/PortalLayout'
import { useAuth } from '../../auth/AuthContext'

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('pl-PL', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function PortalTicketDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const { currentUser } = useAuth()
  const navigate = useNavigate()
  const ticketId = Number(id)

  const [ticket, setTicket] = useState<Ticket | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function load() {
      setError(null)
      try {
        const t = await getTicket(ticketId)
        // Basic access guard: only show if ticket belongs to this user
        if (
          t.requester_email &&
          currentUser?.email &&
          t.requester_email.toLowerCase() !== currentUser.email.toLowerCase()
        ) {
          setError('Nie masz dostępu do tego zgłoszenia.')
          return
        }
        setTicket(t)
      } catch (err) {
        const msg = err instanceof Error ? err.message : 'Nieznany błąd.'
        setError(msg.includes('404') ? 'Nie znaleziono zgłoszenia.' : `Błąd: ${msg}`)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [ticketId, currentUser])

  if (loading) {
    return (
      <PortalLayout>
        <div className="page">
          <LoadingState label="Pobieranie zgłoszenia…" />
        </div>
      </PortalLayout>
    )
  }

  if (error || !ticket) {
    return (
      <PortalLayout>
        <div className="page space-y-4">
          <div className="bg-red-500/10 border border-red-500/30 rounded-xl px-5 py-4 text-sm text-red-400">
            {error ?? 'Nie znaleziono zgłoszenia.'}
          </div>
          <button
            className="text-sm text-gray-400 hover:text-gray-200 transition-colors"
            onClick={() => navigate('/portal/tickets')}
          >
            ← Wróć do listy zgłoszeń
          </button>
        </div>
      </PortalLayout>
    )
  }

  return (
    <PortalLayout>
      <div className="page space-y-6">
        {/* Header */}
        <div className="space-y-2">
          <button
            className="text-xs text-gray-500 hover:text-gray-300 transition-colors flex items-center gap-1"
            onClick={() => navigate('/portal/tickets')}
          >
            ← Wróć do moich zgłoszeń
          </button>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono text-gray-500 bg-white/5 px-2 py-0.5 rounded">
              #{ticket.id}
            </span>
            <StatusBadge status={ticket.status} />
            <SourceBadge source={ticket.source} />
          </div>
          <h1 className="text-xl font-semibold text-gray-100 leading-snug">{ticket.title}</h1>
          <p className="text-xs text-gray-600">Zgłoszono {formatDate(ticket.created_at)}</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
          {/* Left: main content */}
          <div className="lg:col-span-2 space-y-5">
            {/* Description */}
            <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-3">
              <h3 className="text-sm font-semibold text-gray-300">Opis zgłoszenia</h3>
              <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
                {ticket.description || <span className="text-gray-500 italic">Brak opisu.</span>}
              </p>
            </div>

            {/* Agent response */}
            {ticket.agent_response && (
              <div className="bg-surface rounded-xl border border-green-500/20 p-5 space-y-3">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 rounded-full bg-green-400" />
                  <h3 className="text-sm font-semibold text-green-300">Odpowiedź agenta</h3>
                </div>
                <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
                  {ticket.agent_response}
                </p>
              </div>
            )}

            {!ticket.agent_response && (
              <div className="bg-surface rounded-xl border border-white/8 p-5">
                <h3 className="text-sm font-semibold text-gray-300 mb-2">Odpowiedź agenta</h3>
                <p className="text-sm text-gray-500 italic">
                  Twoje zgłoszenie jest w trakcie realizacji. Agent odpowie wkrótce.
                </p>
              </div>
            )}

            {/* AI Response history (read-only) */}
            <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-3">
              <h3 className="text-sm font-semibold text-gray-300">Propozycje AI</h3>
              <AIResponseHistory ticketId={ticket.id} />
            </div>
          </div>

          {/* Right: status panel */}
          <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-4 sticky top-6">
            <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Szczegóły</h2>

            <div className="space-y-3">
              <div className="flex justify-between items-start gap-2">
                <span className="text-xs text-gray-500">Status</span>
                <StatusBadge status={ticket.status} />
              </div>

              <div className="flex justify-between items-start gap-2">
                <span className="text-xs text-gray-500">Źródło</span>
                <SourceBadge source={ticket.source} />
              </div>

              {ticket.requester_email && (
                <div className="flex justify-between items-start gap-2">
                  <span className="text-xs text-gray-500 shrink-0">E-mail</span>
                  <span className="text-xs text-gray-300 text-right break-all">{ticket.requester_email}</span>
                </div>
              )}

              <div className="flex justify-between items-center gap-2">
                <span className="text-xs text-gray-500">Zgłoszono</span>
                <span className="text-xs text-gray-400">{formatDate(ticket.created_at)}</span>
              </div>

              <div className="flex justify-between items-center gap-2">
                <span className="text-xs text-gray-500">Zaktualizowano</span>
                <span className="text-xs text-gray-400">{formatDate(ticket.updated_at)}</span>
              </div>

              {ticket.assigned_agent_name && (
                <div className="flex justify-between items-center gap-2">
                  <span className="text-xs text-gray-500">Agent</span>
                  <span className="text-xs text-gray-300">{ticket.assigned_agent_name}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </PortalLayout>
  )
}

