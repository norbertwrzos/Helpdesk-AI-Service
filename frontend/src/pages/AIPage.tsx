import { useEffect, useState } from 'react'
import { getAIResponseQualityMetrics } from '../api/qualityMetrics'
import type { QualityMetrics } from '../types/qualityMetrics'
import QualityMetricsPanel from '../components/QualityMetricsPanel'
import LoadingState from '../components/LoadingState'

export default function AIPage() {
  const [metrics, setMetrics] = useState<QualityMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getAIResponseQualityMetrics()
      .then(setMetrics)
      .catch((err) =>
        setError(err instanceof Error ? err.message : 'Błąd podczas pobierania metryk.'),
      )
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">AI — Jakość odpowiedzi</h1>
        <p className="page__subtitle">
          Metryki jakości wygenerowanych odpowiedzi AI oraz analiza ewaluacyjna pipeline'u.
        </p>
      </div>

      {loading && <LoadingState label="Pobieranie metryk…" />}
      {error && <div className="alert alert--error">{error}</div>}
      {!loading && !error && metrics && <QualityMetricsPanel metrics={metrics} />}
      {!loading && !error && !metrics && (
        <div className="mt-6 rounded-xl border border-gray-800 bg-gray-900/60 p-6">
          <p className="text-gray-500 text-sm">
            Brak danych. Uruchom analizę zgłoszeń i wystaw oceny AI, aby zobaczyć metryki.
          </p>
        </div>
      )}
    </div>
  )
}
