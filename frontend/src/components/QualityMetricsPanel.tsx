import type { QualityMetrics } from '../types/qualityMetrics'

interface Props {
  metrics: QualityMetrics
}

export default function QualityMetricsPanel({ metrics }: Props) {
  const avgRating = metrics.average_rating !== null ? metrics.average_rating.toFixed(2) : '—'

  return (
    <div className="quality-metrics">
      <div className="quality-metrics__grid">
        <div className="quality-metrics__card">
          <div className="quality-metrics__value">{metrics.total_ai_responses}</div>
          <div className="quality-metrics__label">Wygenerowanych odpowiedzi AI</div>
        </div>
        <div className="quality-metrics__card">
          <div className="quality-metrics__value">{metrics.total_tickets_analyzed}</div>
          <div className="quality-metrics__label">Przeanalizowanych zgłoszeń</div>
        </div>
        <div className="quality-metrics__card">
          <div className="quality-metrics__value">{metrics.total_feedback}</div>
          <div className="quality-metrics__label">Ocenionych odpowiedzi</div>
        </div>
        <div className="quality-metrics__card">
          <div className="quality-metrics__value">{avgRating}</div>
          <div className="quality-metrics__label">Średnia ocena (1-5)</div>
        </div>
        <div className="quality-metrics__card">
          <div className="quality-metrics__value">{metrics.feedback_coverage_percent}%</div>
          <div className="quality-metrics__label">Pokrycie feedbackiem</div>
        </div>
        <div className="quality-metrics__card quality-metrics__card--helpful">
          <div className="quality-metrics__value">{metrics.helpful_count}</div>
          <div className="quality-metrics__label">Odpowiedzi pomocnych</div>
        </div>
        <div className="quality-metrics__card quality-metrics__card--nothelpful">
          <div className="quality-metrics__value">{metrics.not_helpful_count}</div>
          <div className="quality-metrics__label">Odpowiedzi niepomocnych</div>
        </div>
        <div className="quality-metrics__card">
          <div className="quality-metrics__value">{metrics.responses_without_feedback}</div>
          <div className="quality-metrics__label">Odpowiedzi bez oceny</div>
        </div>
      </div>

      <div className="quality-metrics__distribution">
        <h3 className="quality-metrics__dist-title">Rozkład ocen</h3>
        <table className="quality-metrics__dist-table">
          <thead>
            <tr>
              <th>Ocena</th>
              <th>Opis</th>
              <th>Liczba</th>
            </tr>
          </thead>
          <tbody>
            {[
              [5, 'Bardzo dobra'],
              [4, 'Dobra'],
              [3, 'Przeciętna'],
              [2, 'Słaba'],
              [1, 'Bardzo słaba'],
            ].map(([val, label]) => (
              <tr key={val}>
                <td>{'★'.repeat(val as number)}{'☆'.repeat(5 - (val as number))}</td>
                <td>{label}</td>
                <td>{metrics.rating_distribution[String(val)] ?? 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
