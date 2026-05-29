import type { Ticket } from '../types/ticket'
import type { AnalysisResult } from '../types/analysis'
import AgentResponseBox from './AgentResponseBox'
import TicketAiSection from './TicketAiSection'
import TicketTimeline from './TicketTimeline'

interface Props {
  ticket: Ticket
  onAgentResponseSaved: (response: string) => void
  onAnalyzed: (result: AnalysisResult) => void
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('pl-PL', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function TicketMainPanel({ ticket, onAgentResponseSaved, onAnalyzed }: Props) {
  return (
    <div className="space-y-5">
      {/* Description */}
      <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-3">
        <h3 className="text-sm font-semibold text-gray-300">Opis zgłoszenia</h3>
        <p className="text-sm text-gray-300 leading-relaxed whitespace-pre-wrap">
          {ticket.description || <span className="text-gray-500 italic">Brak opisu.</span>}
        </p>
      </div>

      {/* Requester info */}
      {(ticket.requester_name || ticket.requester_email) && (
        <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-3">
          <h3 className="text-sm font-semibold text-gray-300">Dane zgłaszającego</h3>
          <dl className="space-y-2">
            {ticket.requester_name && (
              <div className="flex gap-3 text-sm">
                <dt className="text-gray-500 w-28 shrink-0">Imię i nazwisko</dt>
                <dd className="text-gray-300">{ticket.requester_name}</dd>
              </div>
            )}
            {ticket.requester_email && (
              <div className="flex gap-3 text-sm">
                <dt className="text-gray-500 w-28 shrink-0">E-mail</dt>
                <dd className="text-gray-300 break-all">{ticket.requester_email}</dd>
              </div>
            )}
          </dl>
        </div>
      )}

      {/* Email message info — only for email-source tickets */}
      {ticket.source === 'email' && (
        <div className="bg-surface rounded-xl border border-cyan-500/20 p-5 space-y-3">
          <div className="flex items-center gap-2">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.8} className="w-4 h-4 text-cyan-400">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
              <polyline points="22,6 12,13 2,6"/>
            </svg>
            <h3 className="text-sm font-semibold text-cyan-300">Informacje z wiadomości e-mail</h3>
          </div>
          <dl className="space-y-2">
            {ticket.email_sender && (
              <div className="flex gap-3 text-sm">
                <dt className="text-gray-500 w-28 shrink-0">Nadawca</dt>
                <dd className="text-gray-300 break-all">{ticket.email_sender}</dd>
              </div>
            )}
            {ticket.email_subject && (
              <div className="flex gap-3 text-sm">
                <dt className="text-gray-500 w-28 shrink-0">Temat</dt>
                <dd className="text-gray-300">{ticket.email_subject}</dd>
              </div>
            )}
            {ticket.email_received_at && (
              <div className="flex gap-3 text-sm">
                <dt className="text-gray-500 w-28 shrink-0">Data odebrania</dt>
                <dd className="text-gray-300">{formatDate(ticket.email_received_at)}</dd>
              </div>
            )}
            {ticket.email_message_id && (
              <div className="flex gap-3 text-sm">
                <dt className="text-gray-500 w-28 shrink-0">Message-ID</dt>
                <dd>
                  <details className="group">
                    <summary className="text-xs text-gray-600 cursor-pointer hover:text-gray-400 transition-colors list-none flex items-center gap-1">
                      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-3 h-3 transition-transform group-open:rotate-90">
                        <polyline points="9 18 15 12 9 6"/>
                      </svg>
                      Pokaż
                    </summary>
                    <p className="mt-1 text-xs text-gray-500 font-mono break-all">{ticket.email_message_id}</p>
                  </details>
                </dd>
              </div>
            )}
          </dl>
        </div>
      )}

      {/* Agent response */}
      <AgentResponseBox
        ticketId={ticket.id}
        initialResponse={ticket.agent_response}
        onSaved={onAgentResponseSaved}
      />

      {/* Timeline */}
      <TicketTimeline ticket={ticket} />

      {/* AI section */}
      <TicketAiSection ticket={ticket} onAnalyzed={onAnalyzed} />
    </div>
  )
}
