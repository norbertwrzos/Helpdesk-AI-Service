import type { Feedback } from './feedback'

export interface RagSource {
  article_id: number | null
  title: string
  score: number | null
  excerpt?: string | null
  used_by_model?: boolean | null
  source_type?: string | null
}

export interface ParsedSources {
  sources: RagSource[]
  parse_error?: string | null
}

export interface AIResponse {
  id: number
  ticket_id: number
  response_text: string
  model_name: string
  provider_name: string
  sources_used: string | null
  created_at: string
  feedback?: Feedback | null
}
