import type { TicketMessage } from '../../types/ticketMessage'
import TicketMessageItem from './TicketMessageItem'

interface Props {
  messages: TicketMessage[]
}

export default function TicketMessageList({ messages }: Props) {
  if (messages.length === 0) {
    return (
      <p className="text-sm text-gray-500 italic text-center py-4">
        Brak wiadomości w tym zgłoszeniu.
      </p>
    )
  }

  return (
    <div className="space-y-4">
      {messages.map(msg => (
        <TicketMessageItem key={msg.id} message={msg} />
      ))}
    </div>
  )
}
