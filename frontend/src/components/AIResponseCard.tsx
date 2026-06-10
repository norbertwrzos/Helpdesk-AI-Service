import { useState } from 'react'
import { Link } from 'react-router-dom'
import { createTicketMessage } from '../api/ticketMessages'
import { useAuth } from '../auth/AuthContext'
import { useToast } from '../context/ToastContext'
import type { AIResponse } from '../types/aiResponse'
import type { Feedback } from '../types/feedback'
import { getProviderDisplay } from '../utils/aiProvider'
import { parseSourcesUsed } from '../utils/ragSources'
import { formatDateTime } from '../utils/dateFormat'
import FeedbackForm from './FeedbackForm'
import FeedbackSummary from './FeedbackSummary'

interface Props {
  ticketId: number
  aiResponse: AIResponse
  onSavedAsMessage?: () => void
}

function formatScore(score: number | null | undefined) {
  if (score == null || Number.isNaN(score)) return null
  if (score >= 0 && score <= 1) return `${Math.round(score * 100)}%`
  return score.toFixed(2)
}

export default function AIResponseCard({
  ticketId,
  aiResponse,
  onSavedAsMessage,
}: Props) {
  const [feedback, setFeedback] = useState<Feedback | null>(aiResponse.feedback ?? null)
  const [showForm, setShowForm] = useState(false)
  const [copying, setCopying] = useState(false)
  const [savingAsAgent, setSavingAsAgent] = useState(false)
  const { role, currentUser } = useAuth()
  const { showToast } = useToast()

  const providerDisplay = getProviderDisplay(aiResponse.provider_name)
  const parsedSources = parseSourcesUsed(aiResponse.sources_used)
  const canSaveAsAgent = role === 'agent'

  function handleFeedbackSaved(saved: Feedback) {
    setFeedback(saved)
    setShowForm(false)
  }

  async function handleCopyResponse() {
    if (!navigator.clipboard?.writeText) {
      showToast('Nie udało się skopiować odpowiedzi.', 'error')
      return
    }

    setCopying(true)
    try {
      await navigator.clipboard.writeText(aiResponse.response_text)
      showToast('Skopiowano odpowiedź do schowka.', 'success')
    } catch {
      showToast('Nie udało się skopiować odpowiedzi.', 'error')
    } finally {
      setCopying(false)
    }
  }

  async function handleSaveAsAgentResponse() {
    if (!canSaveAsAgent) {
      return
    }

    setSavingAsAgent(true)
    try {
      await createTicketMessage(ticketId, {
        author_role: 'agent',
        author_name: currentUser?.name ?? 'Agent',
        author_email: currentUser?.email ?? null,
        message_text: aiResponse.response_text,
      })
      onSavedAsMessage?.()
      showToast('Odpowiedź AI została dodana do konwersacji.', 'success')
    } catch {
      showToast('Nie udało się dodać odpowiedzi AI do konwersacji.', 'error')
    } finally {
      setSavingAsAgent(false)
    }
  }

  return (
    <div className="rounded-xl border border-white/8 bg-[#0f1117] p-4 space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        <div className="space-y-2">
          <div className="flex flex-wrap items-center gap-2">
            <span className={`inline-flex items-center rounded-full px-2.5 py-1 text-xs font-medium ${providerDisplay.badgeClassName}`}>
              {providerDisplay.label}
            </span>
            <span className="inline-flex items-center rounded-full border border-cyan-500/25 bg-cyan-500/10 px-2.5 py-1 text-xs font-medium text-cyan-300">
              {aiResponse.model_name || 'Brak modelu'}
            </span>
          </div>
          <div className="text-xs text-gray-500">
            Wygenerowano: {formatDateTime(aiResponse.created_at)}
          </div>
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            className="btn btn--ghost btn--sm"
            onClick={handleCopyResponse}
            disabled={copying}
          >
            {copying ? 'Kopiowanie…' : 'Kopiuj odpowiedź'}
          </button>
          {canSaveAsAgent && (
            <button
              className="btn btn--ghost btn--sm"
              onClick={handleSaveAsAgentResponse}
              disabled={savingAsAgent}
            >
              {savingAsAgent ? 'Zapisywanie…' : 'Dodaj jako wiadomość agenta'}
            </button>
          )}
        </div>
      </div>

      <div className="rounded-lg border border-amber-500/20 bg-amber-500/8 px-3 py-2 text-xs leading-relaxed text-amber-200">
        Treść została wygenerowana przez AI i wymaga weryfikacji agenta przed wysłaniem do zgłaszającego.
      </div>

      <div className="rounded-lg border border-white/8 bg-black/10 p-4">
        <pre className="whitespace-pre-wrap font-sans text-sm leading-relaxed text-gray-200">
          {aiResponse.response_text || 'Brak treści odpowiedzi.'}
        </pre>
      </div>

      <div className="space-y-3">
        <div className="flex items-center justify-between gap-3">
          <h4 className="text-xs font-medium uppercase tracking-[0.18em] text-gray-500">
            Źródła RAG
          </h4>
          {parsedSources.sources.length > 0 && (
            <span className="text-xs text-gray-500">
              {parsedSources.sources.length} {parsedSources.sources.length === 1 ? 'źródło' : 'źródła'}
            </span>
          )}
        </div>

        {parsedSources.parse_error && (
          <div className="rounded-lg border border-yellow-500/20 bg-yellow-500/8 px-3 py-2 text-xs text-yellow-200">
            {parsedSources.parse_error}
          </div>
        )}

        {parsedSources.sources.length > 0 ? (
          <div className="space-y-3">
            {parsedSources.sources.map((source, index) => {
              const scoreLabel = formatScore(source.score)

              return (
                <div key={`${source.article_id ?? 'source'}-${index}`} className="rounded-lg border border-white/8 bg-white/[0.03] p-3 space-y-2">
                  <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                    <div className="space-y-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-sm font-medium text-gray-200">{source.title}</span>
                        {source.used_by_model && (
                          <span className="inline-flex items-center rounded-full border border-emerald-500/25 bg-emerald-500/10 px-2 py-0.5 text-[11px] font-medium text-emerald-300">
                            użyte przez model
                          </span>
                        )}
                      </div>
                      {source.excerpt && (
                        <p className="text-xs leading-relaxed text-gray-400">{source.excerpt}</p>
                      )}
                    </div>

                    <div className="flex shrink-0 flex-wrap items-center gap-2">
                      {scoreLabel && (
                        <span className="inline-flex items-center rounded-full border border-cyan-500/25 bg-cyan-500/10 px-2 py-0.5 text-[11px] font-medium text-cyan-300">
                          Score: {scoreLabel}
                        </span>
                      )}
                      {source.article_id !== null && (
                        <Link
                          to={`/knowledge/${source.article_id}`}
                          className="text-xs text-violet-300 transition-colors hover:text-violet-200"
                        >
                          Otwórz artykuł
                        </Link>
                      )}
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        ) : (
          <div className="rounded-lg border border-white/8 bg-white/[0.03] px-3 py-3 text-sm text-gray-500">
            Brak dostępnych źródeł RAG dla tej odpowiedzi.
          </div>
        )}
      </div>

      <div className="border-t border-white/8 pt-3">
        <div className="text-xs font-medium uppercase tracking-[0.18em] text-gray-500 mb-3">
          Feedback
        </div>

        <div className="space-y-3">
          {feedback ? (
            <>
              <FeedbackSummary feedback={feedback} />
              <button
                className="btn btn--ghost btn--sm"
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
    </div>
  )
}
