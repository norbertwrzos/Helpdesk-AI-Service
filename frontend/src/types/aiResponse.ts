import type { Feedback } from './feedback'

export interface AIResponse {
  id: number
  ticket_id: number
  response_text: string
  model_name: string
  provider_name: string
  sources_used: string | null
  created_at: string
  feedback: Feedback | null
}
