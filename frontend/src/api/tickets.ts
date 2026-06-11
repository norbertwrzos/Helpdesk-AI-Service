import { apiClient } from './client'
import type { Ticket, TicketCreate, TicketUpdate } from '../types/ticket'

export const getTickets = (): Promise<Ticket[]> => apiClient.get('/tickets')

export const getTicket = (id: number): Promise<Ticket> => apiClient.get(`/tickets/${id}`)

export const createTicket = (payload: TicketCreate): Promise<Ticket> =>
  apiClient.post('/tickets', payload)

export const updateTicket = (id: number, payload: TicketUpdate): Promise<Ticket> =>
  apiClient.patch(`/tickets/${id}`, payload)

export const deleteTicket = (id: number): Promise<void> =>
  apiClient.delete(`/tickets/${id}`)
