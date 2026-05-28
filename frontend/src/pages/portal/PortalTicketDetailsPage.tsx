import { useParams, Navigate } from 'react-router-dom'

/**
 * Przekierowuje na widok szczegółów zgłoszenia dostępny dla wszystkich ról.
 */
export default function PortalTicketDetailsPage() {
  const { id } = useParams<{ id: string }>()
  return <Navigate to={`/tickets/${id}`} replace />
}
