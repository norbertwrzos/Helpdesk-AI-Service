import type { ReactNode } from 'react'
import Sidebar from './Sidebar'
import Topbar from './Topbar'
import { useEmailImportPoller } from '../hooks/useEmailImportPoller'

interface Props {
  children: ReactNode
}

export default function AppShell({ children }: Props) {
  useEmailImportPoller()

  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--color-bg)', color: 'var(--color-text)' }}>
      <Sidebar />

      {/* Main area offset by sidebar width */}
      <div className="flex flex-col flex-1 ml-64 min-h-screen overflow-hidden">
        <Topbar />

        {/* Content area below topbar */}
        <main className="flex-1 overflow-y-auto" style={{ marginTop: '64px' }}>
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
