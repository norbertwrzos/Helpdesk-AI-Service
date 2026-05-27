import { apiClient } from './client'
import type { AIResponse } from '../types/analysis'

export const getTicketAiResponses = (ticketId: number): Promise<AIResponse[]> =>
  apiClient.get(`/tickets/${ticketId}/ai-responses`)
