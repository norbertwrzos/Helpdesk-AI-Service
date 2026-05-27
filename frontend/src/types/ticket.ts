export type TicketStatus = 'new' | 'in_analysis' | 'answered' | 'resolved' | 'rejected'
export type TicketSource = 'manual' | 'email' | 'csv'

export interface Ticket {
  id: number
  title: string
  description: string
  status: TicketStatus
  source: TicketSource
  category_id: number | null
  priority_id: number | null
  created_at: string
  updated_at: string
}

export interface TicketCreate {
  title: string
  description: string
  category_id?: number | null
  priority_id?: number | null
  source?: TicketSource
}

export interface TicketUpdate {
  title?: string
  description?: string
  status?: TicketStatus
  category_id?: number | null
  priority_id?: number | null
}
