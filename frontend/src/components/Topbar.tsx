import { useState } from 'react'
import UserMenu from './UserMenu'
import NewTicketModal from './NewTicketModal'

interface Props {
  onMenuClick: () => void
}

export default function Topbar({ onMenuClick }: Props) {
  const [modalOpen, setModalOpen] = useState(false)

  return (
    <>
      <header className="fixed left-0 right-0 top-0 z-10 flex h-16 items-center gap-3 border-b border-white/10 bg-slate-950/80 px-4 shadow-[0_16px_40px_rgba(2,6,23,0.28)] backdrop-blur-xl md:left-64 md:px-6">
        {/* Hamburger — mobile only */}
        <button
          onClick={onMenuClick}
          className="shrink-0 rounded-full border border-white/10 p-2 text-slate-400 transition-colors hover:border-white/20 hover:bg-white/5 hover:text-slate-100 md:hidden"
          aria-label="Menu"
        >
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-5 h-5">
            <line x1="3" y1="6" x2="21" y2="6" />
            <line x1="3" y1="12" x2="21" y2="12" />
            <line x1="3" y1="18" x2="21" y2="18" />
          </svg>
        </button>

        {/* App title (compact, desktop only) */}
        <div className="hidden min-w-0 lg:block">
          
          <div className="text-sm text-slate-400">Panel obsługi zgłoszeń</div>
        </div>

        {/* Search */}
        <div className="max-w-md flex-1 lg:ml-2">
          <div className="relative">
            <span className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500">
              <svg
                className="h-4 w-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth={2}
              >
                <circle cx="11" cy="11" r="8" />
                <line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </span>
            <input
              type="text"
              placeholder="Szukaj zgłoszeń…"
              readOnly
              className="w-full rounded-full border border-white/10 bg-white/[0.04] py-2 pl-9 pr-4 text-sm text-slate-300 placeholder:text-slate-500 focus:outline-none focus:ring-1 focus:ring-violet-400/50"
            />
          </div>
        </div>

        <div className="ml-auto flex shrink-0 items-center gap-2 md:gap-3">
          {/* New ticket button → opens modal */}
          <button
            onClick={() => setModalOpen(true)}
            className="inline-flex items-center gap-1.5 rounded-full border border-violet-300/20 bg-violet-500 px-3.5 py-2 text-sm font-semibold text-white shadow-[0_10px_22px_rgba(15,23,42,0.18)] transition-all hover:-translate-y-px hover:bg-violet-400 hover:shadow-[0_12px_24px_rgba(15,23,42,0.22)] active:translate-y-0"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2.5} className="w-4 h-4 shrink-0">
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            <span className="hidden sm:inline">Nowe zgłoszenie</span>
            <span className="sm:hidden">Nowe</span>
          </button>

          {/* User menu */}
          <div className="border-l border-white/10 pl-2 md:pl-4">
            <UserMenu />
          </div>
        </div>
      </header>

      <NewTicketModal isOpen={modalOpen} onClose={() => setModalOpen(false)} />
    </>
  )
}
