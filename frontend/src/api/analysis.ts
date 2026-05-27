import { apiClient } from './client'
import type { AnalysisResult } from '../types/analysis'

export const analyzeTicket = (ticketId: number): Promise<AnalysisResult> =>
  apiClient.post(`/tickets/${ticketId}/analyze`)
