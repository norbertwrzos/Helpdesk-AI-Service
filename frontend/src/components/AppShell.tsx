import { useState, type ReactNode } from 'react'
import Sidebar from './Sidebar'
import Topbar from './Topbar'

interface Props {
  children: ReactNode
}

export default function AppShell({ children }: Props) {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div
      className="flex h-screen overflow-hidden"
      style={{
        background: 'radial-gradient(circle at top, rgba(99, 102, 241, 0.16) 0%, transparent 30%), radial-gradient(circle at 85% 20%, rgba(34, 211, 238, 0.08) 0%, transparent 24%), var(--color-bg)',
        color: 'var(--color-text)',
      }}
    >
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main area: on md+ offset by sidebar width, on mobile full-width */}
      <div className="flex min-h-screen flex-1 flex-col overflow-hidden md:ml-64">
        <Topbar onMenuClick={() => setSidebarOpen(prev => !prev)} />

        {/* Content area below topbar */}
        <main className="flex-1 overflow-y-auto" style={{ marginTop: '64px' }}>
          <div className="flex min-h-full w-full flex-col p-4 md:p-6 lg:p-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
