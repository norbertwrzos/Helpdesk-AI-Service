export interface Feedback {
  id: number
  ticket_id: number
  ai_response_id: number
  rating: number
  is_helpful: boolean | null
  comment: string | null
  created_at: string
}

export interface FeedbackCreate {
  ai_response_id: number
  rating: number
  is_helpful?: boolean
  comment?: string
}
