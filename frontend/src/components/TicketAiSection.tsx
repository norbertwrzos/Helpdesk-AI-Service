import { useState } from 'react'
import { analyzeTicket } from '../api/analysis'
import type { Ticket } from '../types/ticket'
import type { AnalysisResult } from '../types/analysis'
import AIResponseHistory from './AIResponseHistory'

interface Props {
  ticket: Ticket
  onAnalyzed: (result: AnalysisResult) => void
}

export default function TicketAiSection({ ticket, onAnalyzed }: Props) {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisError, setAnalysisError] = useState<string | null>(null)
  const [aiHistoryKey, setAiHistoryKey] = useState(0)

  async function handleAnalyze() {
    setAnalysisError(null)
    setAnalyzing(true)
    try {
      const result = await analyzeTicket(ticket.id)
      setAnalysisResult(result)
      onAnalyzed(result)
      setAiHistoryKey(k => k + 1)
    } catch (err) {
      setAnalysisError(err instanceof Error ? err.message : 'Błąd podczas analizy.')
    } finally {
      setAnalyzing(false)
    }
  }

  return (
    <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between gap-3">
        <h3 className="text-sm font-semibold text-gray-300">Analiza AI</h3>
        <button
          className="flex items-center gap-1.5 bg-violet-600 hover:bg-violet-500 disabled:opacity-50 text-white text-sm font-medium px-3 py-1.5 rounded-lg transition-colors"
          onClick={handleAnalyze}
          disabled={analyzing}
        >
          <span>🤖</span>
          {analyzing ? 'Analizowanie…' : 'Uruchom analizę AI'}
        </button>
      </div>

      {/* Error */}
      {analysisError && (
        <div className="bg-red-500/10 border border-red-500/30 rounded-lg px-4 py-3 text-sm text-red-400">
          {analysisError}
        </div>
      )}

      {/* Loading */}
      {analyzing && (
        <div className="text-sm text-gray-400 animate-pulse">
          Trwa analiza zgłoszenia, proszę czekać…
        </div>
      )}

      {/* Empty hint */}
      {!analysisResult && !analyzing && !analysisError && (
        <p className="text-sm text-gray-500">
          Kliknij „Uruchom analizę AI", aby automatycznie sklasyfikować zgłoszenie i wygenerować propozycję rozwiązania.
        </p>
      )}

      {/* Results */}
      {analysisResult && !analyzing && (
        <div className="space-y-4">
          {/* Classification + Priority cards */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="bg-[#0f1117] rounded-lg border border-white/8 p-4 space-y-1">
              <div className="text-xs text-gray-500 font-medium uppercase tracking-wider">Kategoria AI</div>
              <div className="text-sm font-semibold text-gray-200">{analysisResult.classification.category_name}</div>
              <div className="text-xs text-violet-400">
                Pewność: {Math.round(analysisResult.classification.confidence * 100)}%
              </div>
              {analysisResult.classification.explanation && (
                <p className="text-xs text-gray-400 mt-1 leading-relaxed">{analysisResult.classification.explanation}</p>
              )}
            </div>

            <div className="bg-[#0f1117] rounded-lg border border-white/8 p-4 space-y-1">
              <div className="text-xs text-gray-500 font-medium uppercase tracking-wider">Priorytet AI</div>
              <div className="text-sm font-semibold text-gray-200">{analysisResult.priority.priority_name}</div>
              <div className="text-xs text-violet-400">
                Pewność: {Math.round(analysisResult.priority.confidence * 100)}%
              </div>
              {analysisResult.priority.explanation && (
                <p className="text-xs text-gray-400 mt-1 leading-relaxed">{analysisResult.priority.explanation}</p>
              )}
            </div>
          </div>

          {/* AI Response proposal */}
          {analysisResult.ai_response && (
            <div className="bg-[#0f1117] rounded-lg border border-violet-500/20 p-4 space-y-2">
              <div className="text-xs text-violet-400 font-medium uppercase tracking-wider">Propozycja rozwiązania</div>
              <div className="text-sm text-gray-300 leading-relaxed space-y-2">
                {analysisResult.ai_response.response_text.split('\n').map((line, i) => (
                  line ? <p key={i}>{line}</p> : <br key={i} />
                ))}
              </div>
              <div className="text-xs text-gray-600">
                Model: {analysisResult.ai_response.model_name} · Provider: {analysisResult.ai_response.provider_name}
              </div>
            </div>
          )}

          {/* Similar articles */}
          {analysisResult.similar_articles.length > 0 && (
            <div className="space-y-2">
              <div className="text-xs text-gray-500 font-medium uppercase tracking-wider">Podobne artykuły w bazie wiedzy</div>
              <ul className="space-y-2">
                {analysisResult.similar_articles.map(article => (
                  <li key={article.id} className="bg-[#0f1117] rounded-lg border border-white/8 px-4 py-3 space-y-1">
                    <div className="flex items-center justify-between gap-2">
                      <span className="text-sm font-medium text-gray-200">{article.title}</span>
                      <span className="text-xs text-cyan-400 shrink-0">
                        {Math.round(article.score * 100)}% dopasowania
                      </span>
                    </div>
                    {article.excerpt && (
                      <p className="text-xs text-gray-400 leading-relaxed">{article.excerpt}</p>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* AI Response History */}
      <div className="pt-2 border-t border-white/8 space-y-3">
        <div className="text-xs text-gray-500 font-medium uppercase tracking-wider">Historia odpowiedzi AI</div>
        <AIResponseHistory ticketId={ticket.id} refreshKey={aiHistoryKey} />
      </div>
    </div>
  )
}
