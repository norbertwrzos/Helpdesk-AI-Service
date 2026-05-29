import { useEffect, useState } from 'react'
import { getEmailImportLogs, getSchedulerStatus, runEmailImport } from '../api/emailImport'
import EmailImportLogsTable from '../components/EmailImportLogsTable'
import type { EmailImportLog, EmailImportRunResponse, EmailImportSchedulerStatus } from '../types/emailImport'

export default function EmailImportPage() {
  const [limit, setLimit] = useState<number>(10)
  const [analyzeImported, setAnalyzeImported] = useState<boolean>(true)
  const [isRunning, setIsRunning] = useState(false)
  const [isLoadingLogs, setIsLoadingLogs] = useState(false)
  const [runResult, setRunResult] = useState<EmailImportRunResponse | null>(null)
  const [logs, setLogs] = useState<EmailImportLog[]>([])
  const [error, setError] = useState<string | null>(null)
  const [logsLoaded, setLogsLoaded] = useState(false)
  const [schedulerStatus, setSchedulerStatus] = useState<EmailImportSchedulerStatus | null>(null)

  useEffect(() => {
    getSchedulerStatus()
      .then(setSchedulerStatus)
      .catch(() => setSchedulerStatus(null))
  }, [])

  async function handleRunImport() {
    setIsRunning(true)
    setError(null)
    setRunResult(null)
    try {
      const result = await runEmailImport({ limit, analyze_imported: analyzeImported })
      setRunResult(result)
      setLogs(result.logs)
      setLogsLoaded(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Nieznany błąd importu.')
    } finally {
      setIsRunning(false)
    }
  }

  async function handleLoadLogs() {
    setIsLoadingLogs(true)
    setError(null)
    try {
      const result = await getEmailImportLogs()
      setLogs(result)
      setLogsLoaded(true)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Nie udało się pobrać logów.')
    } finally {
      setIsLoadingLogs(false)
    }
  }

  return (
    <div className="page">
      <h1 className="page__title">Import zgłoszeń z e-maila</h1>
      <p className="page__description">
        Ta funkcja pobiera wiadomości z testowej skrzynki IMAP (GreenMail) i tworzy na ich
        podstawie zgłoszenia techniczne. Każda wiadomość jest importowana tylko raz — system
        wykrywa i pomija duplikaty.
      </p>

      {/* Status schedulera */}
      {schedulerStatus && (
        <div className={`rounded-xl border p-4 mb-2 flex items-center gap-3 text-sm ${
          schedulerStatus.running
            ? 'border-green-500/30 bg-green-500/5'
            : 'border-gray-700 bg-gray-900/40'
        }`}>
          <span className={`w-2.5 h-2.5 rounded-full shrink-0 ${
            schedulerStatus.running ? 'bg-green-400 animate-pulse' : 'bg-gray-600'
          }`} />
          <div className="flex-1">
            <span className={schedulerStatus.running ? 'text-green-300 font-medium' : 'text-gray-500'}>
              Scheduler {schedulerStatus.running ? 'aktywny' : 'nieaktywny'}
            </span>
            {schedulerStatus.running && (
              <span className="text-gray-500 ml-2">
                — importuje co {schedulerStatus.interval_seconds}s
                {schedulerStatus.auto_analyze && ', z automatyczną analizą AI'}
              </span>
            )}
          </div>
        </div>
      )}

      {/* Formularz importu */}
      <div className="card">
        <h2 className="card__title">Uruchom import</h2>
        <div className="form-group">
          <label htmlFor="limit" className="form-label">
            Limit wiadomości
          </label>
          <input
            id="limit"
            type="number"
            min={1}
            max={100}
            value={limit}
            onChange={(e) => setLimit(Math.max(1, parseInt(e.target.value, 10) || 1))}
            className="form-input form-input--short"
          />
        </div>
        <div className="form-group form-group--checkbox">
          <input
            id="analyzeImported"
            type="checkbox"
            checked={analyzeImported}
            onChange={(e) => setAnalyzeImported(e.target.checked)}
            className="form-checkbox"
          />
          <label htmlFor="analyzeImported" className="form-label">
            Analizuj automatycznie zaimportowane zgłoszenia (mock AI)
          </label>
        </div>
        <button
          onClick={handleRunImport}
          disabled={isRunning}
          className="btn btn--primary"
        >
          {isRunning ? 'Importowanie…' : 'Uruchom import'}
        </button>
      </div>

      {/* Błąd */}
      {error && (
        <div className="alert alert--error">
          <strong>Błąd:</strong> {error}
        </div>
      )}

      {/* Podsumowanie po imporcie */}
      {runResult && (
        <div className="card">
          <h2 className="card__title">Podsumowanie importu</h2>
          <div className="stats-grid">
            <div className="stat-card stat-card--success">
              <div className="stat-card__value">{runResult.imported_count}</div>
              <div className="stat-card__label">Zaimportowanych</div>
            </div>
            <div className="stat-card stat-card--warning">
              <div className="stat-card__value">{runResult.skipped_count}</div>
              <div className="stat-card__label">Pominiętych</div>
            </div>
            <div className="stat-card stat-card--error">
              <div className="stat-card__value">{runResult.error_count}</div>
              <div className="stat-card__label">Błędów</div>
            </div>
            <div className="stat-card stat-card--info">
              <div className="stat-card__value">{runResult.analyzed_count}</div>
              <div className="stat-card__label">Przeanalizowanych</div>
            </div>
          </div>
        </div>
      )}

      {/* Logi importu */}
      <div className="card">
        <div className="card__header">
          <h2 className="card__title">Logi importu</h2>
          <button
            onClick={handleLoadLogs}
            disabled={isLoadingLogs}
            className="btn btn--secondary"
          >
            {isLoadingLogs ? 'Ładowanie…' : 'Odśwież logi'}
          </button>
        </div>

        {!logsLoaded && !isLoadingLogs && (
          <p className="empty-state">
            Kliknij „Uruchom import" lub „Odśwież logi", aby zobaczyć historię importu.
          </p>
        )}

        {isLoadingLogs && <p className="loading-state">Ładowanie logów…</p>}

        {logsLoaded && !isLoadingLogs && (
          <EmailImportLogsTable logs={logs} />
        )}
      </div>
    </div>
  )
}
