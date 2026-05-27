import { useEffect, useState } from 'react'
import { getTickets } from '../api/tickets'
import { getCategories } from '../api/categories'
import { getPriorities } from '../api/priorities'
import type { Ticket } from '../types/ticket'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import TicketForm from '../components/TicketForm'
import TicketList from '../components/TicketList'
import LoadingState from '../components/LoadingState'

export default function TicketsPage() {
  const [tickets, setTickets] = useState<Ticket[]>([])
  const [categories, setCategories] = useState<Category[]>([])
  const [priorities, setPriorities] = useState<Priority[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  async function loadAll() {
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

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Zgłoszenia techniczne</h1>
        <p className="page__subtitle">Lista zgłoszeń zarejestrowanych w systemie helpdesk.</p>
      </div>

      <TicketForm
        categories={categories}
        priorities={priorities}
        onSuccess={loadAll}
      />

      <div className="page__section">
        <h2 className="page__section-title">Lista zgłoszeń</h2>
        {loading && <LoadingState label="Pobieranie zgłoszeń…" />}
        {error && <div className="alert alert--error">{error}</div>}
        {!loading && !error && (
          <TicketList tickets={tickets} categories={categories} priorities={priorities} />
        )}
      </div>
    </div>
  )
}
