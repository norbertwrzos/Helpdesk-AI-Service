import type { TicketMessage } from '../../types/ticketMessage'
import { formatDateTime } from '../../utils/dateFormat'

interface Props {
  message: TicketMessage
}

const ROLE_LABELS: Record<string, string> = {
  agent: 'Agent',
  end_user: 'Użytkownik',
  system: 'System',
}

export default function TicketMessageItem({ message }: Props) {
  const isAgent = message.author_role === 'agent'

  return (
    <div className={`flex flex-col gap-1 ${isAgent ? 'items-end' : 'items-start'}`}>
      {/* Author meta */}
      <div className="flex items-center gap-2 px-1">
        <span className="text-xs font-medium text-gray-300">
          {message.author_name || '—'}
        </span>
        <span
          className={`text-xs px-1.5 py-0.5 rounded-full font-medium ${
            isAgent
              ? 'bg-violet-500/20 text-violet-300'
              : 'bg-white/10 text-gray-400'
          }`}
        >
          {ROLE_LABELS[message.author_role] ?? message.author_role}
        </span>
        <span className="text-xs text-gray-600">
          {formatDateTime(message.created_at)}
        </span>
      </div>

      {/* Message bubble */}
      <div
        className={`max-w-[85%] rounded-xl px-4 py-3 text-sm leading-relaxed whitespace-pre-wrap break-words ${
          isAgent
            ? 'bg-violet-500/10 border border-violet-500/25 text-violet-100'
            : 'bg-white/5 border border-white/10 text-gray-300'
        }`}
      >
        {message.message_text}
      </div>
    </div>
  )
}
