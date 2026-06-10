import { useState } from 'react'
import { createTicketMessage } from '../../api/ticketMessages'
import type { TicketMessage, TicketMessageCreate } from '../../types/ticketMessage'

interface Props {
  ticketId: number
  authorRole: 'agent' | 'end_user'
  authorName: string
  authorEmail?: string | null
  onSent: (message: TicketMessage) => void
}

export default function TicketMessageComposer({
  ticketId,
  authorRole,
  authorName,
  authorEmail,
  onSent,
}: Props) {
  const [text, setText] = useState('')
  const [sending, setSending] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSend() {
    const trimmed = text.trim()
    if (!trimmed) {
      setError('Treść wiadomości nie może być pusta.')
      return
    }

    setError(null)
    setSending(true)
    try {
      const payload: TicketMessageCreate = {
        author_role: authorRole,
        author_name: authorName,
        author_email: authorEmail ?? null,
        message_text: trimmed,
      }
      const created = await createTicketMessage(ticketId, payload)
      setText('')
      onSent(created)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Nie udało się wysłać wiadomości.')
    } finally {
      setSending(false)
    }
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="space-y-2">
      <textarea
        className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2.5 focus:outline-none focus:ring-1 focus:ring-violet-500 resize-y min-h-[80px]"
        value={text}
        onChange={e => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Napisz wiadomość…"
        disabled={sending}
        rows={3}
      />
      {error && <p className="text-xs text-red-400">{error}</p>}
      <div className="flex items-center justify-between">
        <span className="text-xs text-gray-600">Ctrl+Enter aby wysłać</span>
        <button
          className="bg-violet-600 hover:bg-violet-500 disabled:opacity-50 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          onClick={handleSend}
          disabled={sending}
        >
          {sending ? 'Wysyłanie…' : 'Wyślij wiadomość'}
        </button>
      </div>
    </div>
  )
}
