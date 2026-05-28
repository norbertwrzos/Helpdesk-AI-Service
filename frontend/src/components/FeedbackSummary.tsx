import type { Feedback } from '../types/feedback'

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('pl-PL', { dateStyle: 'medium', timeStyle: 'short' })
}

const HELPFUL_LABELS: Record<string, string> = {
  'true': 'Tak',
  'false': 'Nie',
}

interface Props {
  feedback: Feedback
}

export default function FeedbackSummary({ feedback }: Props) {
  return (
    <div className="feedback-summary">
      <div className="feedback-summary__row">
        <span className="feedback-summary__label">Ocena:</span>
        <span className="feedback-summary__rating">
          {'★'.repeat(feedback.rating)}{'☆'.repeat(5 - feedback.rating)}
          {' '}({feedback.rating}/5)
        </span>
      </div>
      {feedback.is_helpful !== null && (
        <div className="feedback-summary__row">
          <span className="feedback-summary__label">Pomocna:</span>
          <span>{HELPFUL_LABELS[String(feedback.is_helpful)]}</span>
        </div>
      )}
      {feedback.comment && (
        <div className="feedback-summary__row">
          <span className="feedback-summary__label">Komentarz:</span>
          <span>{feedback.comment}</span>
        </div>
      )}
      <div className="feedback-summary__row">
        <span className="feedback-summary__label">Data oceny:</span>
        <span>{formatDate(feedback.created_at)}</span>
      </div>
    </div>
  )
}
