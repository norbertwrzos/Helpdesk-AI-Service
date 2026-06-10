import { useEffect, useState } from 'react'
import { getTicketMessages } from '../../api/ticketMessages'
import type { TicketMessage } from '../../types/ticketMessage'
import TicketMessageList from './TicketMessageList'
import TicketMessageComposer from './TicketMessageComposer'

interface Props {
  ticketId: number
  authorRole: 'agent' | 'end_user'
  authorName: string
  authorEmail?: string | null
  title?: string
  /** Increment to force-refresh messages from outside (e.g. after AI response saved) */
  refreshKey?: number
  /** Called whenever a message is successfully sent */
  onMessageSent?: (message: TicketMessage) => void
}

export default function TicketConversation({
  ticketId,
  authorRole,
  authorName,
  authorEmail,
  title = 'Konwersacja',
  refreshKey,
  onMessageSent,
}: Props) {
  const [messages, setMessages] = useState<TicketMessage[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [internalKey, setInternalKey] = useState(0)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    getTicketMessages(ticketId)
      .then(data => {
        if (!cancelled) setMessages(data)
      })
      .catch(() => {
        if (!cancelled) setError('Nie udało się pobrać wiadomości.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [ticketId, refreshKey, internalKey])

  function handleSent(message: TicketMessage) {
    setMessages(prev => [...prev, message])
    onMessageSent?.(message)
  }

  function handleExternalRefresh() {
    setInternalKey(k => k + 1)
  }

  return (
    <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-4">
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-sm font-semibold text-gray-300">{title}</h3>
        <button
          className="text-xs text-gray-500 hover:text-gray-300 transition-colors"
          onClick={handleExternalRefresh}
          title="Odśwież wiadomości"
        >
          Odśwież
        </button>
      </div>

      {loading ? (
        <p className="text-sm text-gray-500 animate-pulse">Pobieranie wiadomości…</p>
      ) : error ? (
        <p className="text-sm text-red-400">{error}</p>
      ) : (
        <TicketMessageList messages={messages} />
      )}

      <div className="pt-3 border-t border-white/8">
        <TicketMessageComposer
          ticketId={ticketId}
          authorRole={authorRole}
          authorName={authorName}
          authorEmail={authorEmail}
          onSent={handleSent}
        />
      </div>
    </div>
  )
}
