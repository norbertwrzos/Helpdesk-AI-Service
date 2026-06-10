import { useEffect, useState } from 'react'
import { getTicketAiResponses } from '../api/aiResponses'
import type { AIResponse } from '../types/aiResponse'
import AIResponseCard from './AIResponseCard'
import EmptyState from './EmptyState'
import ErrorState from './ErrorState'
import LoadingState from './LoadingState'

interface Props {
  ticketId: number
  /** Jeśli true, lista zostanie ponownie pobrana z API */
  refreshKey?: number
  onSavedAsMessage?: () => void
}

export default function AIResponseHistory({
  ticketId,
  refreshKey,
  onSavedAsMessage,
}: Props) {
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

  if (error) return <ErrorState message={error} />

  if (responses.length === 0) {
    return (
      <EmptyState
        message="Brak historii odpowiedzi AI"
        description="Uruchom analizę zgłoszenia, aby wygenerować pierwszą propozycję odpowiedzi i kontekst RAG."
      />
    )
  }

  const [latestResponse, ...olderResponses] = responses

  return (
    <div className="space-y-4">
      <div className="space-y-3">
        <div className="text-xs font-medium uppercase tracking-[0.18em] text-violet-300">
          Najnowsza odpowiedź AI
        </div>
        <AIResponseCard
          key={latestResponse.id}
          ticketId={ticketId}
          aiResponse={latestResponse}
          onSavedAsMessage={onSavedAsMessage}
        />
      </div>

      {olderResponses.length > 0 && (
        <div className="space-y-3">
          <div className="text-xs font-medium uppercase tracking-[0.18em] text-gray-500">
            Starsze odpowiedzi
          </div>
          <div className="space-y-4">
            {olderResponses.map(resp => (
              <AIResponseCard
                key={resp.id}
                ticketId={ticketId}
                aiResponse={resp}
                onSavedAsMessage={onSavedAsMessage}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
