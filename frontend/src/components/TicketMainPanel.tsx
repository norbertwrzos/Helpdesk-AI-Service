import { useState } from 'react'
import type { Ticket } from '../types/ticket'
import type { AnalysisResult } from '../types/analysis'
import TicketAiSection from './TicketAiSection'
import TicketConversation from './tickets/TicketConversation'
import { useAuth } from '../auth/AuthContext'

interface Props {
  ticket: Ticket
  onAnalyzed: (result: AnalysisResult) => void
}

export default function TicketMainPanel({ ticket, onAnalyzed }: Props) {
  const { currentUser } = useAuth()
  const [conversationKey, setConversationKey] = useState(0)

  function handleAiResponseSavedAsMessage() {
    // Refresh conversation so AI responses saved by agent are immediately visible.
    setConversationKey(k => k + 1)
  }

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

      {/* Conversation thread */}
      <TicketConversation
        ticketId={ticket.id}
        authorRole="agent"
        authorName={currentUser?.name ?? 'Agent'}
        authorEmail={currentUser?.email ?? null}
        refreshKey={conversationKey}
      />

      {/* Agent response */}
      <TicketAiSection
        ticket={ticket}
        onAnalyzed={onAnalyzed}
        onSavedAsMessage={handleAiResponseSavedAsMessage}
      />
    </div>
  )
}
