import RoleBasedNavigation from './RoleBasedNavigation'

interface Props {
  isOpen: boolean
  onClose: () => void
}

export default function Sidebar({ isOpen, onClose }: Props) {
  return (
    <>
      {/* Mobile backdrop */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-10 md:hidden"
          onClick={onClose}
          aria-hidden="true"
        />
      )}

      <aside
        className={[
          'fixed left-0 top-0 z-20 flex h-screen w-64 flex-col border-r border-white/10 bg-slate-950/90 backdrop-blur-xl transition-transform duration-200 ease-in-out',
          'md:translate-x-0',
          isOpen ? 'translate-x-0' : '-translate-x-full',
        ].join(' ')}
      >
        {/* Brand */}
        <div className="flex h-16 flex-shrink-0 items-center gap-3 border-b border-white/10 px-5">
          <div className="flex h-9 w-9 items-center justify-center rounded-2xl bg-gradient-to-br from-violet-500 via-violet-400 to-cyan-400 text-sm font-bold text-white shadow-[0_16px_24px_rgba(99,102,241,0.32)]">
            H
          </div>
          <div>
            <div className="leading-none text-sm font-semibold text-slate-100">Helpdesk AI</div>
            <div className="mt-0.5 text-xs text-slate-500">Service</div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 py-4 px-3 overflow-y-auto">
          <RoleBasedNavigation />
        </nav>

        {/* Footer */}
        <div className="flex-shrink-0 border-t border-white/10 px-4 py-3">
          <div className="text-[11px] uppercase tracking-[0.16em] text-slate-600">Prototyp · praca inżynierska</div>
        </div>
      </aside>
    </>
  )
}
