import { useState } from 'react'
import { createOrUpdateFeedback } from '../api/feedback'
import type { Feedback, FeedbackCreate } from '../types/feedback'

const RATING_LABELS: Record<number, string> = {
  1: 'Bardzo słaba',
  2: 'Słaba',
  3: 'Przeciętna',
  4: 'Dobra',
  5: 'Bardzo dobra',
}

interface Props {
  ticketId: number
  aiResponseId: number
  existingFeedback: Feedback | null
  onSaved: (feedback: Feedback) => void
}

export default function FeedbackForm({ ticketId, aiResponseId, existingFeedback, onSaved }: Props) {
  const [rating, setRating] = useState<number>(existingFeedback?.rating ?? 0)
  const [isHelpful, setIsHelpful] = useState<boolean | undefined>(
    existingFeedback?.is_helpful ?? undefined,
  )
  const [comment, setComment] = useState<string>(existingFeedback?.comment ?? '')
  const [saving, setSaving] = useState(false)
  const [success, setSuccess] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    if (rating === 0) {
      setError('Wybierz ocenę w skali 1-5.')
      return
    }
    setError(null)
    setSuccess(false)
    setSaving(true)
    try {
      const payload: FeedbackCreate = {
        ai_response_id: aiResponseId,
        rating,
        is_helpful: isHelpful,
        comment: comment.trim() || undefined,
      }
      const saved = await createOrUpdateFeedback(ticketId, payload)
      setSuccess(true)
      onSaved(saved)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd podczas zapisywania oceny.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <form className="feedback-form" onSubmit={handleSubmit} noValidate>
      <h4 className="feedback-form__title">
        {existingFeedback ? 'Zaktualizuj ocenę' : 'Oceń odpowiedź AI'}
      </h4>

      {error && <div className="alert alert--error">{error}</div>}
      {success && <div className="alert alert--success">Ocena została zapisana.</div>}

      <div className="form-group">
        <label className="form-label">Ocena</label>
        <div className="feedback-form__ratings">
          {[1, 2, 3, 4, 5].map(val => (
            <button
              key={val}
              type="button"
              className={`feedback-form__rating-btn${rating === val ? ' feedback-form__rating-btn--active' : ''}`}
              onClick={() => setRating(val)}
              title={RATING_LABELS[val]}
            >
              <span className="feedback-form__rating-number">{val}</span>
              <span className="feedback-form__rating-label">{RATING_LABELS[val]}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="form-group">
        <label className="form-label">Czy odpowiedź była pomocna?</label>
        <div className="feedback-form__helpful">
          <label className="feedback-form__helpful-option">
            <input
              type="radio"
              name={`helpful-${aiResponseId}`}
              checked={isHelpful === true}
              onChange={() => setIsHelpful(true)}
            />
            {' '}Tak
          </label>
          <label className="feedback-form__helpful-option">
            <input
              type="radio"
              name={`helpful-${aiResponseId}`}
              checked={isHelpful === false}
              onChange={() => setIsHelpful(false)}
            />
            {' '}Nie
          </label>
        </div>
      </div>

      <div className="form-group">
        <label className="form-label" htmlFor={`comment-${aiResponseId}`}>
          Komentarz (opcjonalny)
        </label>
        <textarea
          id={`comment-${aiResponseId}`}
          className="form-input form-textarea"
          value={comment}
          onChange={e => setComment(e.target.value)}
          rows={3}
          placeholder="Opisz, czy odpowiedź była trafna…"
        />
      </div>

      <button className="btn btn--primary" type="submit" disabled={saving}>
        {saving ? 'Zapisywanie…' : 'Zapisz ocenę'}
      </button>
    </form>
  )
}
