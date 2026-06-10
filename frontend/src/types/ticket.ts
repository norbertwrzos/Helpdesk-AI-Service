export type TicketStatus = 'open' | 'ai_reviewed' | 'pending' | 'resolved' | 'rejected'
export type TicketSource = 'manual'

export const TICKET_STATUS_LABELS: Record<TicketStatus, string> = {
  open: 'Otwarte',
  ai_reviewed: 'Zweryfikowane przez AI',
  pending: 'Oczekujące',
  resolved: 'Rozwiązane',
  rejected: 'Odrzucone',
}

export interface Ticket {
  id: number
  title: string
  description: string
  status: TicketStatus
  source: TicketSource
  category_id: number | null
  priority_id: number | null
  requester_email: string | null
  requester_name: string | null
  assigned_agent_name: string | null
  classification_confidence: number | null
  priority_confidence: number | null
  classification_explanation: string | null
  priority_explanation: string | null
  created_at: string
  updated_at: string
}

export interface TicketCreate {
  title: string
  description: string
  requester_email: string
  requester_name?: string | null
  category_id?: number | null
  priority_id?: number | null
}

export interface TicketUpdate {
  title?: string
  description?: string
  status?: TicketStatus
  category_id?: number | null
  priority_id?: number | null
  assigned_agent_name?: string | null
}
