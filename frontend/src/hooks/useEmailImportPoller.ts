import { useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { getEmailImportLogs } from '../api/emailImport'
import { useToast } from '../context/ToastContext'

const POLL_INTERVAL_MS = 30_000

/**
 * Polls /email/import/logs?limit=1 every 30s.
 * When a new "imported" log appears, shows a toast.
 * Clicking the toast navigates to /tickets and triggers a hard reload
 * so the ticket list picks up the new entry.
 */
export function useEmailImportPoller() {
  const { showToast } = useToast()
  const navigate = useNavigate()
  const lastLogIdRef = useRef<number | null>(null)
  const initializedRef = useRef(false)

  useEffect(() => {
    async function poll() {
      try {
        const logs = await getEmailImportLogs()
        const latest = logs[0] ?? null

        if (!initializedRef.current) {
          // First run — just record the current latest ID, no toast
          lastLogIdRef.current = latest?.id ?? null
          initializedRef.current = true
          return
        }

        if (
          latest &&
          latest.status === 'imported' &&
          latest.id !== lastLogIdRef.current
        ) {
          lastLogIdRef.current = latest.id
          const subject = latest.subject ?? 'nowa wiadomość'
          const sender = latest.sender ?? ''
          const msg = sender
            ? `Nowe zgłoszenie z e-maila: „${subject}" od ${sender}`
            : `Nowe zgłoszenie z e-maila: „${subject}"`

          showToast(msg, 'info', () => {
            navigate('/tickets')
            // Small delay so navigate completes, then force refresh of the page
            setTimeout(() => window.location.reload(), 50)
          })
        }
      } catch {
        // Silently ignore — don't spam the user with polling errors
      }
    }

    // Initial check immediately, then on interval
    poll()
    const id = setInterval(poll, POLL_INTERVAL_MS)
    return () => clearInterval(id)
  }, [showToast, navigate])
}
