import { useState } from 'react'
import { Link } from 'react-router-dom'
import { updateTicket } from '../api/tickets'
import { analyzeTicket } from '../api/analysis'
import type { Ticket, TicketStatus, TicketUpdate } from '../types/ticket'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import type { AnalysisResult } from '../types/analysis'
import TicketStatusBadge from './TicketStatusBadge'
import TicketSourceBadge from './TicketSourceBadge'

interface Props {
  ticket: Ticket
  categories: Category[]
  priorities: Priority[]
  onUpdated: (updated: Ticket) => void
}

const STATUS_OPTIONS: { value: TicketStatus; label: string }[] = [
  { value: 'new', label: 'Nowe' },
  { value: 'in_analysis', label: 'W analizie' },
  { value: 'answered', label: 'Odpowiedziane' },
  { value: 'resolved', label: 'Rozwiązane' },
  { value: 'rejected', label: 'Odrzucone' },
]

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('pl-PL', { dateStyle: 'medium', timeStyle: 'short' })
}

export default function TicketDetails({ ticket, categories, priorities, onUpdated }: Props) {
  const [title, setTitle] = useState(ticket.title)
  const [description, setDescription] = useState(ticket.description)
  const [status, setStatus] = useState<TicketStatus>(ticket.status)
  const [categoryId, setCategoryId] = useState<string>(ticket.category_id?.toString() ?? '')
  const [priorityId, setPriorityId] = useState<string>(ticket.priority_id?.toString() ?? '')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisError, setAnalysisError] = useState<string | null>(null)

  const categoryMap = Object.fromEntries(categories.map(c => [c.id, c.name]))
  const priorityMap = Object.fromEntries(priorities.map(p => [p.id, p.name]))

  async function handleAnalyze() {
    setAnalysisError(null)
    setAnalyzing(true)
    try {
      const result = await analyzeTicket(ticket.id)
      setAnalysisResult(result)
      // Odśwież ticket, żeby pokazać zaktualizowany status i kategorię
      onUpdated({
        ...ticket,
        status: 'answered',
        category_id: result.classification.category_id,
        priority_id: result.priority.priority_id,
        classification_confidence: result.classification.confidence,
        priority_confidence: result.priority.confidence,
        classification_explanation: result.classification.explanation,
        priority_explanation: result.priority.explanation,
      })
    } catch (err) {
      setAnalysisError(err instanceof Error ? err.message : 'Błąd podczas analizy.')
    } finally {
      setAnalyzing(false)
    }
  }

  async function handleSave(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setSuccess(false)

    const payload: TicketUpdate = {
      title: title.trim(),
      description: description.trim(),
      status,
      category_id: categoryId ? Number(categoryId) : null,
      priority_id: priorityId ? Number(priorityId) : null,
    }

    setSaving(true)
    try {
      const updated = await updateTicket(ticket.id, payload)
      setSuccess(true)
      onUpdated(updated)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd podczas zapisywania.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="ticket-details">
      <div className="ticket-details__header">
        <div className="ticket-details__id-row">
          <span className="ticket-card__id">#{ticket.id}</span>
          <TicketStatusBadge status={ticket.status} />
          <TicketSourceBadge source={ticket.source} />
        </div>
        <h1 className="ticket-details__main-title">{ticket.title}</h1>
      </div>

      <div className="ticket-details__meta-grid">
        <div className="ticket-details__meta-item">
          <span className="ticket-details__meta-label">Kategoria</span>
          <span>{ticket.category_id ? (categoryMap[ticket.category_id] ?? `#${ticket.category_id}`) : '—'}</span>
        </div>
        <div className="ticket-details__meta-item">
          <span className="ticket-details__meta-label">Priorytet</span>
          <span>{ticket.priority_id ? (priorityMap[ticket.priority_id] ?? `#${ticket.priority_id}`) : '—'}</span>
        </div>
        <div className="ticket-details__meta-item">
          <span className="ticket-details__meta-label">Utworzono</span>
          <span>{formatDate(ticket.created_at)}</span>
        </div>
        <div className="ticket-details__meta-item">
          <span className="ticket-details__meta-label">Zaktualizowano</span>
          <span>{formatDate(ticket.updated_at)}</span>
        </div>
      </div>

      <div className="ticket-details__description">
        <h2 className="ticket-details__section-title">Opis zgłoszenia</h2>
        <p className="ticket-details__description-text">{ticket.description}</p>
      </div>

      <div className="ticket-details__ai-section">
        <div className="ticket-details__ai-header">
          <h2 className="ticket-details__section-title">Analiza AI</h2>
          <button
            className="btn btn--primary"
            onClick={handleAnalyze}
            disabled={analyzing}
          >
            {analyzing ? 'Analizowanie…' : '🤖 Analizuj zgłoszenie'}
          </button>
        </div>

        {analysisError && (
          <div className="alert alert--error" style={{ marginTop: '12px' }}>
            Błąd analizy: {analysisError}
          </div>
        )}

        {analyzing && (
          <div className="ticket-details__ai-loading">
            Trwa analiza zgłoszenia, proszę czekać…
          </div>
        )}

        {analysisResult && !analyzing && (
          <div className="ticket-details__ai-result">
            <div className="ai-result__grid">
              <div className="ai-result__card">
                <div className="ai-result__label">Kategoria AI</div>
                <div className="ai-result__value">{analysisResult.classification.category_name}</div>
                <div className="ai-result__confidence">
                  Pewność: {Math.round(analysisResult.classification.confidence * 100)}%
                </div>
                <div className="ai-result__explanation">{analysisResult.classification.explanation}</div>
              </div>

              <div className="ai-result__card">
                <div className="ai-result__label">Priorytet AI</div>
                <div className="ai-result__value">{analysisResult.priority.priority_name}</div>
                <div className="ai-result__confidence">
                  Pewność: {Math.round(analysisResult.priority.confidence * 100)}%
                </div>
                <div className="ai-result__explanation">{analysisResult.priority.explanation}</div>
              </div>
            </div>

            {analysisResult.similar_articles.length > 0 && (
              <div className="ai-result__section">
                <h3 className="ai-result__section-title">Podobne artykuły w bazie wiedzy</h3>
                <ul className="ai-result__articles">
                  {analysisResult.similar_articles.map(article => (
                    <li key={article.id} className="ai-result__article-item">
                      <strong>{article.title}</strong>
                      <span className="ai-result__article-score">
                        {' '}(dopasowanie: {Math.round(article.score * 100)}%)
                      </span>
                      <p className="ai-result__article-excerpt">{article.excerpt}</p>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <div className="ai-result__section">
              <h3 className="ai-result__section-title">Propozycja rozwiązania</h3>
              <div className="ai-result__response-text">
                {analysisResult.ai_response.response_text.split('\n').map((line, i) => (
                  <p key={i}>{line}</p>
                ))}
              </div>
              <div className="ai-result__meta">
                Model: {analysisResult.ai_response.model_name} | Provider: {analysisResult.ai_response.provider_name}
              </div>
            </div>
          </div>
        )}

        {!analysisResult && !analyzing && !analysisError && (
          <p className="ticket-details__ai-hint">
            Kliknij „Analizuj zgłoszenie", aby uruchomić automatyczną klasyfikację i wygenerować propozycję rozwiązania.
          </p>
        )}
      </div>

      <form className="ticket-form" onSubmit={handleSave} noValidate>
        <h2 className="ticket-form__title">Edytuj zgłoszenie</h2>

        {error && <div className="alert alert--error">{error}</div>}
        {success && <div className="alert alert--success">Zmiany zostały zapisane.</div>}

        <div className="form-group">
          <label className="form-label" htmlFor="edit-title">Tytuł</label>
          <input
            id="edit-title"
            className="form-input"
            type="text"
            value={title}
            onChange={e => setTitle(e.target.value)}
            maxLength={255}
          />
        </div>

        <div className="form-group">
          <label className="form-label" htmlFor="edit-description">Opis</label>
          <textarea
            id="edit-description"
            className="form-input form-textarea"
            value={description}
            onChange={e => setDescription(e.target.value)}
            rows={4}
          />
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label" htmlFor="edit-status">Status</label>
            <select
              id="edit-status"
              className="form-input form-select"
              value={status}
              onChange={e => setStatus(e.target.value as TicketStatus)}
            >
              {STATUS_OPTIONS.map(o => (
                <option key={o.value} value={o.value}>{o.label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="edit-category">Kategoria</label>
            <select
              id="edit-category"
              className="form-input form-select"
              value={categoryId}
              onChange={e => setCategoryId(e.target.value)}
            >
              <option value="">— brak —</option>
              {categories.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label className="form-label" htmlFor="edit-priority">Priorytet</label>
            <select
              id="edit-priority"
              className="form-input form-select"
              value={priorityId}
              onChange={e => setPriorityId(e.target.value)}
            >
              <option value="">— brak —</option>
              {priorities.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>
        </div>

        <div className="form-actions">
          <button className="btn btn--primary" type="submit" disabled={saving}>
            {saving ? 'Zapisywanie…' : 'Zapisz zmiany'}
          </button>
          <Link to="/tickets" className="btn btn--ghost">
            ← Wróć do listy
          </Link>
        </div>
      </form>
    </div>
  )
}
