import { apiClient } from './client'
import type {
  EmailImportLog,
  EmailImportRunRequest,
  EmailImportRunResponse,
} from '../types/emailImport'

export function runEmailImport(
  payload: EmailImportRunRequest = { limit: 10, analyze_imported: true },
): Promise<EmailImportRunResponse> {
  return apiClient.post<EmailImportRunResponse>('/email/import/run', payload)
}

export function getEmailImportLogs(): Promise<EmailImportLog[]> {
  return apiClient.get<EmailImportLog[]>('/email/import/logs')
}
