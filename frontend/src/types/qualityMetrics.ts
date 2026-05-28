export interface QualityMetrics {
  total_ai_responses: number
  total_tickets_analyzed: number
  total_feedback: number
  average_rating: number | null
  helpful_count: number
  not_helpful_count: number
  feedback_coverage_percent: number
  rating_distribution: Record<string, number>
  responses_without_feedback: number
}
