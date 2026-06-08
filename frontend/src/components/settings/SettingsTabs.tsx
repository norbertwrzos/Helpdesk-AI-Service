type TabKey = 'categories' | 'priorities' | 'profile'

const TABS: { key: TabKey; label: string }[] = [
  { key: 'categories', label: 'Kategorie' },
  { key: 'priorities', label: 'Priorytety' },
  { key: 'profile',    label: 'Profil' },
]

interface Props {
  active: TabKey
  onChange: (tab: TabKey) => void
}

export default function SettingsTabs({ active, onChange }: Props) {
  return (
    <div className="mb-6 flex gap-2 overflow-x-auto rounded-full border border-white/10 bg-white/[0.03] p-1">
      {TABS.map(tab => (
        <button
          key={tab.key}
          onClick={() => onChange(tab.key)}
          className={[
            'shrink-0 whitespace-nowrap rounded-full px-4 py-2 text-sm font-medium transition-all',
            active === tab.key
              ? 'bg-white/[0.08] text-white shadow-[0_12px_20px_rgba(15,23,42,0.22)]'
              : 'text-gray-500 hover:bg-white/[0.04] hover:text-gray-300',
          ].join(' ')}
        >
          {tab.label}
        </button>
      ))}
    </div>
  )
}

export type { TabKey }
