import type { QualityMetrics } from '../types/qualityMetrics'
import StatCard from './StatCard'

interface Props {
  metrics: QualityMetrics
}

export default function AIMetricsCards({ metrics }: Props) {
  const avg =
    metrics.average_rating != null
      ? metrics.average_rating.toFixed(2)
      : '—'

  const cards = [
    {
      label: 'Wygenerowane odpowiedzi',
      value: metrics.total_ai_responses,
      valueColor: 'text-violet-400',
    },
    {
      label: 'Ocenione odpowiedzi',
      value: metrics.total_feedback,
      valueColor: 'text-blue-400',
    },
    {
      label: 'Średnia ocena',
      value: avg,
      valueColor:
        metrics.average_rating == null
          ? 'text-gray-500'
          : metrics.average_rating >= 4
          ? 'text-emerald-400'
          : metrics.average_rating >= 3
          ? 'text-yellow-400'
          : 'text-red-400',
      description: 'w skali 1–5',
    },
    {
      label: 'Pomocne odpowiedzi',
      value: metrics.helpful_count,
      valueColor: 'text-emerald-400',
    },
    {
      label: 'Bez oceny',
      value: metrics.responses_without_feedback,
      valueColor: 'text-gray-400',
    },
  ]

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
      {cards.map((card) => (
        <StatCard
          key={card.label}
          label={card.label}
          value={card.value}
          valueColor={card.valueColor}
          description={card.description}
        />
      ))}
    </div>
  )
}
