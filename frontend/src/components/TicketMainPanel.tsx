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
