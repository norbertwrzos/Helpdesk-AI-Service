import type { MockUser } from '../types/auth'

export const MOCK_USERS: MockUser[] = [
  {
    id: 'admin-1',
    email: 'admin@helpdesk.local',
    name: 'Administrator',
    role: 'admin',
  },
  {
    id: 'agent-1',
    email: 'agent@helpdesk.local',
    name: 'Norbert',
    role: 'agent',
  },
  {
    id: 'user-1',
    email: 'user@company.local',
    name: 'Jan',
    role: 'end_user',
  },
]
