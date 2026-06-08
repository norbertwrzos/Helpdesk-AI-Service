import { useEffect, useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import { getTickets } from '../api/tickets'
import type { Ticket } from '../types/ticket'
import StatCard from '../components/StatCard'
import RecentTickets from '../components/RecentTickets'
import QuickActions from '../components/QuickActions'

export default function DashboardPage() {
  const { currentUser } = useAuth()
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    getTickets()
      .then(setTickets)
      .catch(() => setError('Nie udało się załadować zgłoszeń.'))
      .finally(() => setLoading(false))
  }, [])

  const total = tickets.length
  const open = tickets.filter((t) => t.status === 'open').length
  const aiReviewed = tickets.filter((t) => t.status === 'ai_reviewed').length
  const pending = tickets.filter((t) => t.status === 'pending').length

  const recent = [...tickets]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5)

  return (
    <div className="page">
      {/* Header */}
      <div className="page__header">
        <h1 className="page__title">
          Witaj, {currentUser?.name ?? 'użytkowniku'}
        </h1>
        <p className="page__subtitle">
          Panel obsługi zgłoszeń technicznych.
        </p>
      </div>

      {/* Stat cards */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
          {[...Array(4)].map((_, i) => (
            <div
              key={i}
              className="surface-card h-24 animate-pulse"
            />
          ))}
        </div>
      ) : error ? (
        <div className="mt-6 rounded-2xl border border-red-500/20 bg-red-500/10 p-4 text-sm text-red-300">
          {error}
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
          <StatCard
            label="Wszystkie zgłoszenia"
            value={total}
            valueColor="text-gray-100"
            description="Łącznie w systemie"
          />
          <StatCard
            label="Otwarte"
            value={open}
            valueColor="text-violet-400"
            description="Nowe, nieprzetworzone"
          />
          <StatCard
            label="Zweryfikowane przez AI"
            value={aiReviewed}
            valueColor="text-blue-400"
            description="Po analizie pipeline'u"
          />
          <StatCard
            label="Oczekujące"
            value={pending}
            valueColor="text-yellow-400"
            description="Wymagają działania agenta"
          />
        </div>
      )}

      {/* Recent tickets */}
      <div className="surface-card surface-card--padded mt-8">
        <h2 className="section-heading mb-4">
          Ostatnie zgłoszenia
        </h2>
        {loading ? (
          <div className="space-y-2">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-8 rounded bg-gray-800/60 animate-pulse" />
            ))}
          </div>
        ) : error ? (
          <p className="text-sm text-gray-500">Brak danych.</p>
        ) : (
          <RecentTickets tickets={recent} />
        )}
      </div>

      {/* Quick actions */}
      <div className="surface-card surface-card--padded mt-6">
        <h2 className="section-heading mb-4">
          Szybkie akcje
        </h2>
        <QuickActions />
      </div>
    </div>
  )
}
