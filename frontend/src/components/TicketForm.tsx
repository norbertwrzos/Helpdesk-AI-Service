import { useState } from 'react'
import { createTicket } from '../api/tickets'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import type { TicketCreate } from '../types/ticket'

interface Props {
  categories: Category[]
  priorities: Priority[]
  onSuccess: () => void
}

export default function TicketForm({ categories, priorities, onSuccess }: Props) {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [categoryId, setCategoryId] = useState<string>('')
  const [priorityId, setPriorityId] = useState<string>('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)
    setSuccess(false)

    if (!title.trim()) {
      setError('Tytuł jest wymagany.')
      return
    }
    if (!description.trim()) {
      setError('Opis jest wymagany.')
      return
    }

    const payload: TicketCreate = {
      title: title.trim(),
      description: description.trim(),
      source: 'manual',
      category_id: categoryId ? Number(categoryId) : null,
      priority_id: priorityId ? Number(priorityId) : null,
    }

    setSubmitting(true)
    try {
      await createTicket(payload)
      setTitle('')
      setDescription('')
      setCategoryId('')
      setPriorityId('')
      setSuccess(true)
      onSuccess()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Wystąpił błąd podczas dodawania zgłoszenia.')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <form className="ticket-form" onSubmit={handleSubmit} noValidate>
      <h2 className="ticket-form__title">Nowe zgłoszenie</h2>

      {error && <div className="alert alert--error">{error}</div>}
      {success && <div className="alert alert--success">Zgłoszenie zostało dodane.</div>}

      <div className="form-group">
        <label className="form-label" htmlFor="title">
          Tytuł <span className="form-required">*</span>
        </label>
        <input
          id="title"
          className="form-input"
          type="text"
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Krótki opis problemu…"
          maxLength={255}
        />
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor="description">
          Opis <span className="form-required">*</span>
        </label>
        <textarea
          id="description"
          className="form-input form-textarea"
          value={description}
          onChange={e => setDescription(e.target.value)}
          placeholder="Szczegółowy opis problemu…"
          rows={4}
        />
      </div>

      <div className="form-row">
        <div className="form-group">
          <label className="form-label" htmlFor="category">Kategoria</label>
          <select
            id="category"
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
          <label className="form-label" htmlFor="priority">Priorytet</label>
          <select
            id="priority"
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

      <button className="btn btn--primary" type="submit" disabled={submitting}>
        {submitting ? 'Dodawanie…' : 'Dodaj zgłoszenie'}
      </button>
    </form>
  )
}
