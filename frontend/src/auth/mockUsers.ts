import type { MockUser } from '../types/auth'

export const MOCK_USERS: MockUser[] = [
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
