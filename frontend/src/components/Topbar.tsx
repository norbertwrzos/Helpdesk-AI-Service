import { useState } from 'react'
import { useAuth } from '../auth/AuthContext'
import UserMenu from './UserMenu'
import NewTicketModal from './NewTicketModal'

export default function Topbar() {
  const { role } = useAuth()
  const [modalOpen, setModalOpen] = useState(false)

  // end_user sees a simplified label in the portal context
  const buttonLabel = role === 'end_user' ? 'Nowe zgłoszenie' : 'Nowe zgłoszenie'

  return (
    <>
      <header className="fixed top-0 left-64 right-0 h-16 bg-sidebar border-b border-gray-800 flex items-center px-6 gap-4 z-10">
        {/* App title (compact) */}
        <span className="text-sm font-semibold text-gray-400 hidden lg:block whitespace-nowrap">
          Helpdesk AI Service
        </span>

        {/* Search */}
        <div className="flex-1 max-w-sm ml-4">
          <div className="relative">
            <svg
              className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-600"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth={2}
            >
              <circle cx="11" cy="11" r="8" />
              <line x1="21" y1="21" x2="16.65" y2="16.65" />
            </svg>
            <input
              type="text"
              placeholder="Szukaj zgłoszeń…"
              readOnly
              className="w-full bg-gray-800/50 border border-gray-700 rounded-lg pl-9 pr-4 py-1.5 text-sm text-gray-400 placeholder-gray-600 focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500/50 cursor-text transition-colors"
            />
          </div>
        </div>

        <div className="flex items-center gap-3 ml-auto">
          {/* New ticket button → opens modal */}
          <button
            onClick={() => setModalOpen(true)}
            className="flex items-center gap-2 bg-violet-600 hover:bg-violet-700 active:bg-violet-800 text-white text-sm font-medium px-4 py-1.5 rounded-lg transition-colors whitespace-nowrap"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} className="w-4 h-4">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            {buttonLabel}
          </button>

          {/* User menu */}
          <div className="border-l border-gray-800 pl-4">
            <UserMenu />
          </div>
        </div>
      </header>

      <NewTicketModal isOpen={modalOpen} onClose={() => setModalOpen(false)} />
    </>
  )
}
