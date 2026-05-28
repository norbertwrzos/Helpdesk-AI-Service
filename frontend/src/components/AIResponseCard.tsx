import { useState } from 'react'
import type { AIResponse } from '../types/aiResponse'
import type { Feedback } from '../types/feedback'
import FeedbackForm from './FeedbackForm'
import FeedbackSummary from './FeedbackSummary'

function formatDate(iso: string) {
  return new Date(iso).toLocaleString('pl-PL', { dateStyle: 'medium', timeStyle: 'short' })
}

interface Props {
  ticketId: number
  aiResponse: AIResponse
}

export default function AIResponseCard({ ticketId, aiResponse }: Props) {
  const [feedback, setFeedback] = useState<Feedback | null>(aiResponse.feedback)
  const [showForm, setShowForm] = useState(false)

  function handleFeedbackSaved(saved: Feedback) {
    setFeedback(saved)
    setShowForm(false)
  }

  return (
    <div className="ai-response-card">
      <div className="ai-response-card__header">
        <span className="ai-response-card__date">{formatDate(aiResponse.created_at)}</span>
        <span className="ai-response-card__meta">
          {aiResponse.provider_name} / {aiResponse.model_name}
        </span>
      </div>

      <div className="ai-response-card__text">
        {aiResponse.response_text.split('\n').map((line, i) => (
          <p key={i}>{line}</p>
        ))}
      </div>

      {aiResponse.sources_used && (
        <div className="ai-response-card__sources">
          <strong>Źródła:</strong> {aiResponse.sources_used}
        </div>
      )}

      <div className="ai-response-card__feedback">
        {feedback ? (
          <>
            <FeedbackSummary feedback={feedback} />
            <button
              className="btn btn--ghost btn--sm"
              style={{ marginTop: '8px' }}
              onClick={() => setShowForm(prev => !prev)}
            >
              {showForm ? 'Anuluj' : 'Zmień ocenę'}
            </button>
          </>
        ) : (
          <button
            className="btn btn--ghost btn--sm"
            onClick={() => setShowForm(prev => !prev)}
          >
            {showForm ? 'Anuluj' : '+ Dodaj ocenę'}
          </button>
        )}

        {showForm && (
          <FeedbackForm
            ticketId={ticketId}
            aiResponseId={aiResponse.id}
            existingFeedback={feedback}
            onSaved={handleFeedbackSaved}
          />
        )}
      </div>
    </div>
  )
}
