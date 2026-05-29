import type { QualityMetrics } from '../types/qualityMetrics'

interface Props {
  metrics: QualityMetrics
}

interface CardProps {
  label: string
  value: number | string
  accent?: string
  sub?: string
}

function MetricCard({ label, value, accent = 'text-violet-400', sub }: CardProps) {
  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-5 flex flex-col gap-1">
      <div className={`text-3xl font-bold tabular-nums ${accent}`}>{value}</div>
      <div className="text-sm font-medium text-gray-300">{label}</div>
      {sub && <div className="text-xs text-gray-500 mt-0.5">{sub}</div>}
    </div>
  )
}

export default function AIMetricsCards({ metrics }: Props) {
  const avg =
    metrics.average_rating != null
      ? metrics.average_rating.toFixed(2)
      : '—'

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      <MetricCard
        label="Wygenerowane odpowiedzi"
        value={metrics.total_ai_responses}
      />
      <MetricCard
        label="Ocenione odpowiedzi"
        value={metrics.total_feedback}
        accent="text-blue-400"
      />
      <MetricCard
        label="Średnia ocena"
        value={avg}
        accent={
          metrics.average_rating == null
            ? 'text-gray-500'
            : metrics.average_rating >= 4
            ? 'text-emerald-400'
            : metrics.average_rating >= 3
            ? 'text-yellow-400'
            : 'text-red-400'
        }
        sub="w skali 1–5"
      />
      <MetricCard
        label="Pomocne odpowiedzi"
        value={metrics.helpful_count}
        accent="text-emerald-400"
      />
      <MetricCard
        label="Bez oceny"
        value={metrics.responses_without_feedback}
        accent="text-gray-400"
      />
    </div>
  )
}
