import { Link } from 'react-router-dom'
import type { AIResponse } from '../types/aiResponse'
import { getProviderDisplay } from '../utils/aiProvider'

interface Props {
  responses: AIResponse[]
}

function ratingBadge(rating: number | undefined | null) {
  if (rating == null) {
    return (
      <span className="inline-block px-2 py-0.5 rounded text-xs bg-gray-800 text-gray-500">
        brak
      </span>
    )
  }
  const color =
    rating >= 4
      ? 'bg-emerald-900/60 text-emerald-300'
      : rating >= 3
      ? 'bg-yellow-900/60 text-yellow-300'
      : 'bg-red-900/60 text-red-300'
  return (
    <span className={`inline-block px-2 py-0.5 rounded text-xs font-semibold ${color}`}>
      {rating}/5
    </span>
  )
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('pl-PL', {
    day: '2-digit',
    month: '2-digit',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  })
}

export default function RecentAIResponses({ responses }: Props) {
  if (responses.length === 0) {
    return (
      <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-6">
        <p className="text-sm text-gray-500">
          Brak odpowiedzi AI. Uruchom analizę z widoku szczegółów zgłoszenia.
        </p>
      </div>
    )
  }

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/60 overflow-hidden">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-gray-800 text-left text-xs text-gray-500 uppercase tracking-wider">
              <th className="px-4 py-3 font-medium">Zgłoszenie</th>
              <th className="px-4 py-3 font-medium">Data</th>
              <th className="px-4 py-3 font-medium">Model / Provider</th>
              <th className="px-4 py-3 font-medium">Ocena</th>
              <th className="px-4 py-3 font-medium"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-800">
            {responses.map((r) => (
              <tr key={r.id} className="hover:bg-gray-800/40 transition-colors">
                <td className="px-4 py-3 text-gray-300 font-mono">#{r.ticket_id}</td>
                <td className="px-4 py-3 text-gray-400 whitespace-nowrap">
                  {formatDate(r.created_at)}
                </td>
                <td className="px-4 py-3">
                  <div className="flex flex-wrap items-center gap-2">
                    <span className="text-violet-300">{r.model_name}</span>
                    <span className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${getProviderDisplay(r.provider_name).badgeClassName}`}>
                      {getProviderDisplay(r.provider_name).label}
                    </span>
                  </div>
                </td>
                <td className="px-4 py-3">
                  {ratingBadge(r.feedback?.rating)}
                </td>
                <td className="px-4 py-3 text-right">
                  <Link
                    to={`/tickets/${r.ticket_id}`}
                    className="text-xs text-violet-400 hover:text-violet-300 underline underline-offset-2"
                  >
                    Otwórz →
                  </Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
