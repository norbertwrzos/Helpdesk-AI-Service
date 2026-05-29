import { useEffect, useState } from 'react'
import { getAIResponseQualityMetrics } from '../api/qualityMetrics'
import { getRecentAIResponses } from '../api/aiResponses'
import type { QualityMetrics } from '../types/qualityMetrics'
import type { AIResponse } from '../types/aiResponse'
import AIMetricsCards from '../components/AIMetricsCards'
import RecentAIResponses from '../components/RecentAIResponses'
import AIModuleInfo from '../components/AIModuleInfo'
import LoadingState from '../components/LoadingState'

export default function AIPage() {
  const [metrics, setMetrics] = useState<QualityMetrics | null>(null)
  const [responses, setResponses] = useState<AIResponse[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([
      getAIResponseQualityMetrics(),
      getRecentAIResponses(10),
    ])
      .then(([m, r]) => {
        setMetrics(m)
        setResponses(r)
      })
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
          Panel prezentuje jakość odpowiedzi i podstawowe informacje o module analizy zgłoszeń.
        </p>
      </div>

      {loading && <LoadingState label="Pobieranie danych…" />}
      {error && <div className="alert alert--error">{error}</div>}

      {!loading && !error && (
        <div className="flex flex-col gap-8">
          {/* Metrics */}
          {metrics ? (
            <AIMetricsCards metrics={metrics} />
          ) : (
            <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-6">
              <p className="text-sm text-gray-500">
                Brak metryk. Uruchom analizę zgłoszeń i wystaw oceny AI, aby zobaczyć dane.
              </p>
            </div>
          )}

          {/* Recent AI Responses */}
          <section>
            <h2 className="text-base font-semibold text-gray-200 mb-3">Ostatnie odpowiedzi AI</h2>
            <RecentAIResponses responses={responses} />
          </section>

          {/* Module Info */}
          <section>
            <h2 className="text-base font-semibold text-gray-200 mb-3">Informacja o module</h2>
            <AIModuleInfo />
          </section>
        </div>
      )}
    </div>
  )
}

