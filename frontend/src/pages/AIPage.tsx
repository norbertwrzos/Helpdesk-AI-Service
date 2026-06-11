import { useEffect, useState } from 'react'
import { getRecentAIResponses } from '../api/aiResponses'
import type { AIResponse } from '../types/aiResponse'
import RecentAIResponses from '../components/RecentAIResponses'
import LoadingState from '../components/LoadingState'

export default function AIPage() {
  const [responses, setResponses] = useState<AIResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getRecentAIResponses(10)
      .then(setResponses)
      .catch((err) =>
        setError(err instanceof Error ? err.message : 'Błąd podczas pobierania danych.'),
      )
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">AI</h1>
        <p className="page__subtitle">
          Ostatnie odpowiedzi wygenerowane przez moduł analizy zgłoszeń.
        </p>
      </div>

      {loading && <LoadingState label="Pobieranie danych…" />}
      {error && <div className="rounded-2xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300">{error}</div>}

      {!loading && !error && (
        <section className="space-y-3">
          <h2 className="section-heading">Ostatnie odpowiedzi AI</h2>
          <RecentAIResponses responses={responses} />
        </section>
      )}
    </div>
  )
}

