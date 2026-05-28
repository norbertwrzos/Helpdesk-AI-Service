import { apiClient } from './client'
import type { Feedback, FeedbackCreate } from '../types/feedback'

export const createOrUpdateFeedback = (
  ticketId: number,
  payload: FeedbackCreate,
): Promise<Feedback> =>
  apiClient.post(`/tickets/${ticketId}/feedback`, payload)

export const getTicketFeedback = (ticketId: number): Promise<Feedback[]> =>
  apiClient.get(`/tickets/${ticketId}/feedback`)

export const getAIResponseFeedback = (
  aiResponseId: number,
): Promise<Feedback | null> =>
  apiClient.get(`/ai-responses/${aiResponseId}/feedback`)
