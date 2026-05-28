import { apiClient } from './client'
import type { QualityMetrics } from '../types/qualityMetrics'

export const getAIResponseQualityMetrics = (): Promise<QualityMetrics> =>
  apiClient.get('/quality/ai-responses')
