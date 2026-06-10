import { apiClient } from './client'
import type { TicketMessage, TicketMessageCreate } from '../types/ticketMessage'

export const getTicketMessages = (ticketId: number): Promise<TicketMessage[]> =>
  apiClient.get(`/tickets/${ticketId}/messages`)

export const createTicketMessage = (
  ticketId: number,
  payload: TicketMessageCreate,
): Promise<TicketMessage> => apiClient.post(`/tickets/${ticketId}/messages`, payload)
