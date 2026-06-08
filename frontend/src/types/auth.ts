export type UserRole = 'agent' | 'end_user'

export interface MockUser {
  id: string
  email: string
  name: string
  role: UserRole
}
