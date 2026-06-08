import { useEffect, useMemo, useState } from 'react'
import { getTickets } from '../api/tickets'
import { getCategories } from '../api/categories'
import { getPriorities } from '../api/priorities'
import type { Ticket } from '../types/ticket'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import TicketsTable from '../components/TicketsTable'
import TicketsFilters, { EMPTY_FILTERS, type FilterState } from '../components/TicketsFilters'
import TicketQuickViews, { applyQuickView, type QuickView } from '../components/TicketQuickViews'
import LoadingState from '../components/LoadingState'
import ErrorState from '../components/ErrorState'

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [priorities, setPriorities] = useState<Priority[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const [quickView, setQuickView] = useState<QuickView>('all')
  const [filters, setFilters] = useState<FilterState>(EMPTY_FILTERS)

  async function loadAll() {
    setLoading(true)
    setError(null)
    try {
      const [t, c, p] = await Promise.all([getTickets(), getCategories(), getPriorities()])
      setTickets(t)
      setCategories(c)
      setPriorities(p)
    } catch (err) {
      setError(
        err instanceof Error
          ? `Nie można połączyć się z backendem: ${err.message}`
          : 'Nieznany błąd połączenia.',
      )
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { loadAll() }, [])

  // Quick view counts (on full ticket set)
  const quickCounts = useMemo(() => ({
    all: tickets.length,
    open: tickets.filter(t => t.status === 'open').length,
    ai_reviewed: tickets.filter(t => t.status === 'ai_reviewed').length,
    pending: tickets.filter(t => t.status === 'pending').length,
    resolved: tickets.filter(t => t.status === 'resolved').length,
  }), [tickets])

  // Apply quick view first, then filters
  const filtered = useMemo(() => {
    let result = applyQuickView(tickets, quickView)

    if (filters.search) {
      const q = filters.search.toLowerCase()
      result = result.filter(t =>
        t.title.toLowerCase().includes(q) || t.description.toLowerCase().includes(q),
      )
    }
    if (filters.status) {
      result = result.filter(t => t.status === filters.status)
    }
    if (filters.priorityId) {
      result = result.filter(t => t.priority_id === Number(filters.priorityId))
    }
    if (filters.categoryId) {
      result = result.filter(t => t.category_id === Number(filters.categoryId))
    }
    if (filters.source) {
      result = result.filter(t => t.source === filters.source)
    }
    if (filters.dateFrom) {
      const from = new Date(filters.dateFrom).getTime()
      result = result.filter(t => new Date(t.created_at).getTime() >= from)
    }
    if (filters.dateTo) {
      // include the entire "to" day
      const to = new Date(filters.dateTo).getTime() + 86_400_000
      result = result.filter(t => new Date(t.created_at).getTime() <= to)
    }

    return [...result].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    )
  }, [tickets, quickView, filters])

  return (
    <div className="page">
      {/* Header */}
      <div className="page__header">
        <h1 className="page__title">Zgłoszenia</h1>
        <p className="page__subtitle">
          {loading ? 'Pobieranie danych…' : `${filtered.length} z ${tickets.length} zgłoszeń`}
        </p>
      </div>

      {/* Quick views */}
      <TicketQuickViews
        active={quickView}
        counts={quickCounts}
        onChange={view => {
          setQuickView(view)
          // reset status filter when switching to a status quick view
          if (view !== 'all') {
            setFilters(f => ({ ...f, status: '' }))
          }
        }}
      />

      {/* Filters */}
      <TicketsFilters
        filters={filters}
        categories={categories}
        priorities={priorities}
        onChange={setFilters}
        onReset={() => setFilters(EMPTY_FILTERS)}
      />

      {/* Table */}
      {loading && <LoadingState label="Pobieranie zgłoszeń…" />}
      {!loading && error && <ErrorState message={error} onRetry={loadAll} />}
      {!loading && !error && (
        <TicketsTable
          tickets={filtered}
          categories={categories}
          priorities={priorities}
        />
      )}
    </div>
  )
}
