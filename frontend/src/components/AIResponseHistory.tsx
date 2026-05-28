import { useEffect, useState } from 'react'
import { getTicketAiResponses } from '../api/aiResponses'
import type { AIResponse } from '../types/aiResponse'
import AIResponseCard from './AIResponseCard'
import LoadingState from './LoadingState'

interface Props {
  ticketId: number
  /** Jeśli true, lista zostanie ponownie pobrana z API */
  refreshKey?: number
}

export default function AIResponseHistory({ ticketId, refreshKey }: Props) {
  const [responses, setResponses] = useState<AIResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    setLoading(true)
    setError(null)
    getTicketAiResponses(ticketId)
      .then(data => {
        if (!cancelled) setResponses(data)
      })
      .catch(err => {
        if (!cancelled)
          setError(err instanceof Error ? err.message : 'Błąd podczas pobierania odpowiedzi AI.')
      })
      .finally(() => {
        if (!cancelled) setLoading(false)
      })
    return () => {
      cancelled = true
    }
  }, [ticketId, refreshKey])

  if (loading) return <LoadingState label="Pobieranie historii odpowiedzi AI…" />

  if (error) return <div className="alert alert--error">{error}</div>

  if (responses.length === 0) {
    return (
      <p className="ticket-details__ai-hint">
        Brak wygenerowanych odpowiedzi AI. Uruchom analizę zgłoszenia, aby wygenerować pierwszą odpowiedź.
      </p>
    )
  }

  return (
    <div className="ai-response-history">
      {responses.map(resp => (
        <AIResponseCard key={resp.id} ticketId={ticketId} aiResponse={resp} />
      ))}
    </div>
  )
}
