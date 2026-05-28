import { useEffect, useState } from 'react'
import { getAIResponseQualityMetrics } from '../api/qualityMetrics'
import type { QualityMetrics } from '../types/qualityMetrics'
import QualityMetricsPanel from '../components/QualityMetricsPanel'
import LoadingState from '../components/LoadingState'

export default function QualityPage() {
  const [metrics, setMetrics] = useState<QualityMetrics | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getAIResponseQualityMetrics()
      .then(setMetrics)
      .catch(err =>
        setError(err instanceof Error ? err.message : 'Błąd podczas pobierania metryk.'),
      )
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Jakość odpowiedzi AI</h1>
        <p className="page__description">
          Sekcja prezentuje podstawowe metryki ocen wygenerowanych odpowiedzi AI.
          Dane opierają się na ocenach wystawionych przez użytkowników w skali 1–5.
        </p>
      </div>

      {loading && <LoadingState label="Pobieranie metryk…" />}
      {error && <div className="alert alert--error">{error}</div>}
      {metrics && !loading && <QualityMetricsPanel metrics={metrics} />}
    </div>
  )
}
