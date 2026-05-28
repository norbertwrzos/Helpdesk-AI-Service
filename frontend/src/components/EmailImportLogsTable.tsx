import { Link } from 'react-router-dom'
import type { EmailImportLog } from '../types/emailImport'

interface Props {
  logs: EmailImportLog[]
}

const STATUS_LABEL: Record<EmailImportLog['status'], string> = {
  imported: 'Zaimportowano',
  skipped: 'Pominięto',
  error: 'Błąd',
}

const STATUS_CLASS: Record<EmailImportLog['status'], string> = {
  imported: 'badge badge--success',
  skipped: 'badge badge--warning',
  error: 'badge badge--error',
}

export default function EmailImportLogsTable({ logs }: Props) {
  if (logs.length === 0) {
    return <p className="empty-state">Brak logów importu.</p>
  }

  return (
    <div className="table-wrapper">
      <table className="data-table">
        <thead>
          <tr>
            <th>Data</th>
            <th>Nadawca</th>
            <th>Temat</th>
            <th>Status</th>
            <th>Zgłoszenie</th>
            <th>Błąd</th>
          </tr>
        </thead>
        <tbody>
          {logs.map((log) => (
            <tr key={log.id}>
              <td>{new Date(log.created_at).toLocaleString('pl-PL')}</td>
              <td>{log.sender ?? '—'}</td>
              <td>{log.subject ?? '—'}</td>
              <td>
                <span className={STATUS_CLASS[log.status]}>
                  {STATUS_LABEL[log.status]}
                </span>
              </td>
              <td>
                {log.ticket_id != null ? (
                  <Link to={`/tickets/${log.ticket_id}`}>#{log.ticket_id}</Link>
                ) : (
                  '—'
                )}
              </td>
              <td className="error-cell">{log.error_message ?? '—'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
