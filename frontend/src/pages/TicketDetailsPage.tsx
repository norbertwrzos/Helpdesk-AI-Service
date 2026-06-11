import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getTicket, updateTicket, deleteTicket } from '../api/tickets'
import { getCategories } from '../api/categories'
import { getPriorities } from '../api/priorities'
import type { Ticket, TicketUpdate } from '../types/ticket'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import type { AnalysisResult } from '../types/analysis'
import LoadingState from '../components/LoadingState'
import StatusBadge from '../components/StatusBadge'
import SourceBadge from '../components/SourceBadge'
import TicketMainPanel from '../components/TicketMainPanel'
import TicketPropertiesPanel from '../components/TicketPropertiesPanel'
import TicketTimeline from '../components/TicketTimeline'

export default function TicketDetailsPage() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
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

  async function handleUpdate(update: TicketUpdate) {
    if (!ticket) return
    const updated = await updateTicket(ticket.id, update)
    setTicket(updated)
  }

  async function handleDelete() {
    if (!ticket) return
    await deleteTicket(ticket.id)
    navigate('/tickets')
  }

  function handleAnalyzed(result: AnalysisResult) {
    if (!ticket) return
    setTicket({
      ...ticket,
      status: 'ai_reviewed',
      category_id: result.classification.category_id,
      priority_id: result.priority.priority_id,
      classification_confidence: result.classification.confidence,
      priority_confidence: result.priority.confidence,
      classification_explanation: result.classification.explanation,
      priority_explanation: result.priority.explanation,
    })
  }

  if (loading) {
    return (
      <div className="page">
        <LoadingState label="Pobieranie zgłoszenia…" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="page space-y-4">
        <div className="bg-red-500/10 border border-red-500/30 rounded-xl px-5 py-4 text-sm text-red-400">
          {error}
        </div>
        <button
          className="text-sm text-gray-400 hover:text-gray-200 transition-colors"
          onClick={() => navigate('/tickets')}
        >
          ← Wróć do listy zgłoszeń
        </button>
      </div>
    )
  }

  if (!ticket) return null

  return (
    <div className="page space-y-6">
      {/* Header */}
      <div className="flex items-start justify-between gap-4">
        <div className="space-y-2 min-w-0">
          <button
            className="text-xs text-gray-500 hover:text-gray-300 transition-colors flex items-center gap-1"
            onClick={() => navigate('/tickets')}
          >
            ← Wróć do listy zgłoszeń
          </button>
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-xs font-mono text-gray-500 bg-white/5 px-2 py-0.5 rounded">
              #{ticket.id}
            </span>
            <StatusBadge status={ticket.status} />
            <SourceBadge source={ticket.source} />
          </div>
          <h1 className="text-xl font-semibold text-gray-100 leading-snug">
            {ticket.title}
          </h1>
        </div>
      </div>

      {/* Two-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">
        {/* Left: main content */}
        <div className="lg:col-span-2">
          <TicketMainPanel
            ticket={ticket}
            onAnalyzed={handleAnalyzed}
          />
        </div>

        {/* Right: properties + timeline — sticky scrollable sidebar */}
        <div className="lg:col-span-1">
          <div className="sticky top-6 max-h-[calc(100vh-3rem)] overflow-y-auto space-y-6 pr-1">
          <TicketPropertiesPanel
            ticket={ticket}
            categories={categories}
            priorities={priorities}
            onUpdate={handleUpdate}
            onDelete={handleDelete}
          />
          <TicketTimeline ticket={ticket} />
          </div>
        </div>
      </div>
    </div>
  )
}
