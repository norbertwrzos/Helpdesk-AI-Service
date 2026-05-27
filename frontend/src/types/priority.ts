export interface Priority {
  id: number
  name: string
  level: number
  description?: string | null
  created_at?: string
}

export interface PriorityCreate {
  name: string
  level: number
  description?: string | null
}
