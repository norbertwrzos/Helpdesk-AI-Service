import { useEffect, useState } from 'react'
import { getTicketAiResponses } from '../api/aiResponses'
import { getTicketMessages } from '../api/ticketMessages'
import type { Ticket } from '../types/ticket'
import type { AIResponse } from '../types/aiResponse'
import type { TicketMessage } from '../types/ticketMessage'
import TimelineItem, { type TimelineEvent } from './TimelineItem'

interface Props {
  ticket: Ticket
}

function buildEvents(
  ticket: Ticket,
  aiResponses: AIResponse[],
  ticketMessages: TicketMessage[],
): TimelineEvent[] {
  const events: TimelineEvent[] = []
  const createdAt = new Date(ticket.created_at)
  const updatedAt = new Date(ticket.updated_at)

  events.push({
    id: 'created',
    label: 'Zgłoszenie utworzone',
    sublabel: ticket.source === 'manual'
      ? 'Zgłoszenie dodane ręcznie'
      : ticket.source === 'csv'
      ? 'Zgłoszenie zaimportowane z pliku CSV'
      : undefined,
    date: createdAt,
    iconType: 'ticket',
  })

  events.push({
    id: 'open',
    label: 'Status ustawiony: Otwarte',
    date: createdAt,
    iconType: 'open',
  })

  const sortedResponses = [...aiResponses].sort(
    (a, b) => new Date(a.created_at).getTime() - new Date(b.created_at).getTime(),
  )

  sortedResponses.forEach((resp, idx) => {
    const aiDate = new Date(resp.created_at)
    const isFirst = idx === 0

    // "Analiza AI wykonana" only for the first response
    if (isFirst) {
      events.push({
        id: `ai-analysis-${resp.id}`,
        label: 'Analiza AI wykonana',
        sublabel: ticket.category_id
          ? 'Kategoria i priorytet zaproponowane'
          : undefined,
        date: aiDate,
        iconType: 'ai',
      })

      // Category assigned (after first AI analysis)
      if (ticket.category_id) {
        events.push({
          id: 'category',
          label: 'Kategoria przypisana',
          date: aiDate,
          iconType: 'category',
        })
      }

      // Priority assigned (after first AI analysis)
      if (ticket.priority_id) {
        events.push({
          id: 'priority',
          label: 'Priorytet przypisany',
          date: aiDate,
          iconType: 'priority',
        })
      }
    }

    // AI response generated
    events.push({
      id: `ai-response-${resp.id}`,
      label: 'Odpowiedź AI wygenerowana',
      sublabel: `Model: ${resp.model_name}`,
      date: aiDate,
      iconType: 'ai-response',
    })
  })

  // If no AI responses but category/priority exist — show them based on updated_at
  if (aiResponses.length === 0) {
    if (ticket.category_id) {
      events.push({
        id: 'category',
        label: 'Kategoria przypisana',
        date: updatedAt,
        iconType: 'category',
      })
    }
    if (ticket.priority_id) {
      events.push({
        id: 'priority',
        label: 'Priorytet przypisany',
        date: updatedAt,
        iconType: 'priority',
      })
    }
  }

  // Agent response event inferred from conversation history
  const latestAgentMessage = [...ticketMessages]
    .filter(msg => msg.author_role === 'agent')
    .sort(
      (a, b) =>
        new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    )[0]

  if (latestAgentMessage) {
    events.push({
      id: 'agent',
      label: 'Odpowiedź agenta dodana',
      date: new Date(latestAgentMessage.created_at),
      iconType: 'agent',
    })
  }

  // Resolved
  if (ticket.status === 'resolved') {
    events.push({
      id: 'resolved',
      label: 'Zgłoszenie rozwiązane',
      date: updatedAt,
      iconType: 'resolved',
    })
  }

  // Sort by date ascending; for same-date events keep insertion order
  events.sort((a, b) => a.date.getTime() - b.date.getTime())

  return events
}

export default function TicketTimeline({ ticket }: Props) {
  const [aiResponses, setAiResponses] = useState<AIResponse[]>([])
  const [ticketMessages, setTicketMessages] = useState<TicketMessage[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    Promise.all([
      getTicketAiResponses(ticket.id),
      getTicketMessages(ticket.id),
    ])
      .then(([responses, messages]) => {
        if (cancelled) return
        setAiResponses(responses)
        setTicketMessages(messages)
      })
      .catch(() => { /* non-critical — timeline still works without AI data */ })
      .finally(() => { if (!cancelled) setLoading(false) })
    return () => { cancelled = true }
  }, [ticket.id])

  const events = buildEvents(ticket, aiResponses, ticketMessages)

  return (
    <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-1">
      <h3 className="text-sm font-semibold text-gray-300 mb-4">Historia zdarzenia</h3>

      {loading && (
        <p className="text-xs text-gray-500 animate-pulse">Ładowanie historii…</p>
      )}

      {!loading && events.map((event, idx) => (
        <TimelineItem
          key={event.id}
          event={event}
          isLast={idx === events.length - 1}
        />
      ))}
    </div>
  )
}
