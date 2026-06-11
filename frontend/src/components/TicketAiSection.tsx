import { useEffect, useState } from 'react'
import { analyzeTicket } from '../api/analysis'
import { getTicketAiResponses } from '../api/aiResponses'
import type { Ticket } from '../types/ticket'
import type { AnalysisResult } from '../types/analysis'
import AIResponseHistory from './AIResponseHistory'

interface Props {
  ticket: Ticket
  onAnalyzed: (result: AnalysisResult) => void
  onSavedAsMessage?: () => void
}

export default function TicketAiSection({ ticket, onAnalyzed, onSavedAsMessage }: Props) {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [analyzing, setAnalyzing] = useState(false)
  const [analysisError, setAnalysisError] = useState<string | null>(null)
  const [aiHistoryKey, setAiHistoryKey] = useState(0)
  const [hasExistingAnalysis, setHasExistingAnalysis] = useState(false)

  useEffect(() => {
    getTicketAiResponses(ticket.id)
      .then(data => setHasExistingAnalysis(data.length > 0))
      .catch(() => {})
  }, [ticket.id])

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
          className="flex items-center gap-1.5 bg-violet-600 hover:bg-violet-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-sm font-medium px-3 py-1.5 rounded-lg transition-colors"
          onClick={handleAnalyze}
          disabled={analyzing || hasExistingAnalysis}
          title={hasExistingAnalysis ? 'Analiza AI została już przeprowadzona dla tego zgłoszenia' : undefined}
        >
          {hasExistingAnalysis ? 'Analiza wykonana' : analyzing ? 'Analizowanie…' : 'Uruchom analizę AI'}
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

      

      {/* Results */}
      {analysisResult && !analyzing && (
        <div className="space-y-4">
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

          <div className="rounded-lg border border-violet-500/20 bg-violet-500/8 px-4 py-3 text-sm text-violet-100">
            Analiza została zakończona. Najnowsza odpowiedź AI i źródła RAG są widoczne w historii poniżej.
          </div>
        </div>
      )}

      <div className="pt-2 border-t border-white/8 space-y-3">
        <AIResponseHistory
          ticketId={ticket.id}
          refreshKey={aiHistoryKey}
          onSavedAsMessage={onSavedAsMessage}
        />
      </div>
    </div>
  )
}
