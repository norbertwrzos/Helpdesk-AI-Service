export interface ClassificationResult {
  category_id: number | null
  category_name: string
  confidence: number
  explanation: string
}

export interface PriorityResult {
  priority_id: number | null
  priority_name: string
  confidence: number
  explanation: string
}

export interface SimilarArticle {
  id: number
  title: string
  excerpt: string
  category_id: number | null
  score: number
}

export interface GeneratedAnswer {
  response_text: string
  model_name: string
  provider_name: string
  sources_used: string | null
}

export interface AnalysisResult {
  ticket_id: number
  classification: ClassificationResult
  priority: PriorityResult
  similar_articles: SimilarArticle[]
  ai_response: GeneratedAnswer
}
