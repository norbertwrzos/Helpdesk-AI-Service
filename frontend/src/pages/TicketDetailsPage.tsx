import { useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getTicket } from '../api/tickets'
import { getCategories } from '../api/categories'
import { getPriorities } from '../api/priorities'
import type { Ticket } from '../types/ticket'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import TicketDetails from '../components/TicketDetails'
import LoadingState from '../components/LoadingState'

export default function TicketDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const ticketId = Number(id)

  const [ticket, setTicket] = useState<Ticket | null>(null)
  const [categories, setCategories] = useState<Category[]>([])
  const [priorities, setPriorities] = useState<Priority[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    async function load() {
      setError(null)
      try {
        const [t, c, p] = await Promise.all([
          getTicket(ticketId),
          getCategories(),
          getPriorities(),
        ])
        setTicket(t)
        setCategories(c)
        setPriorities(p)
      } catch (err) {
        const msg = err instanceof Error ? err.message : 'Nieznany błąd.'
        setError(msg.includes('404') ? 'Nie znaleziono zgłoszenia.' : `Błąd: ${msg}`)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [ticketId])

  if (loading) return <div className="page"><LoadingState label="Pobieranie zgłoszenia…" /></div>

  if (error) {
    return (
      <div className="page">
        <div className="alert alert--error">{error}</div>
        <Link to="/tickets" className="btn btn--ghost" style={{ marginTop: '16px' }}>
          ← Wróć do listy
        </Link>
      </div>
    )
  }

  if (!ticket) return null

  return (
    <div className="page">
      <TicketDetails
        ticket={ticket}
        categories={categories}
        priorities={priorities}
        onUpdated={setTicket}
      />
    </div>
  )
}
