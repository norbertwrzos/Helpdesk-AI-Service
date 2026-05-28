export interface EmailImportLog {
  id: number
  message_id: string | null
  sender: string | null
  subject: string | null
  status: 'imported' | 'skipped' | 'error'
  ticket_id: number | null
  error_message: string | null
  created_at: string
}

export interface EmailImportRunResponse {
  imported_count: number
  skipped_count: number
  error_count: number
  analyzed_count: number
  logs: EmailImportLog[]
}

export interface EmailImportRunRequest {
  limit?: number
  analyze_imported?: boolean
}
