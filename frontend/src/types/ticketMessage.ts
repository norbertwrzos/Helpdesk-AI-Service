export type AuthorRole = 'agent' | 'end_user' | 'system'

export interface TicketMessage {
  id: number
  ticket_id: number
  author_role: AuthorRole
  author_name: string
  author_email?: string | null
  message_text: string
  message_type: string
  created_at: string
  updated_at?: string | null
}

export interface TicketMessageCreate {
  author_role: 'agent' | 'end_user'
  author_name: string
  author_email?: string | null
  message_text: string
}
