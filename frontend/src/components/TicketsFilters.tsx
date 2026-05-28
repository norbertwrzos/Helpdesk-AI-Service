import type { TicketStatus, TicketSource } from '../types/ticket'
import { TICKET_STATUS_LABELS } from '../types/ticket'
import { SOURCE_LABELS } from './SourceBadge'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'

export interface FilterState {
  search: string
  status: TicketStatus | ''
  priorityId: string
  categoryId: string
  source: TicketSource | ''
  dateFrom: string
  dateTo: string
}

export const EMPTY_FILTERS: FilterState = {
  search: '',
  status: '',
  priorityId: '',
  categoryId: '',
  source: '',
  dateFrom: '',
  dateTo: '',
}

interface Props {
  filters: FilterState
  categories: Category[]
  priorities: Priority[]
  onChange: (f: FilterState) => void
  onReset: () => void
}

const STATUS_OPTIONS = Object.entries(TICKET_STATUS_LABELS) as [TicketStatus, string][]
const SOURCE_OPTIONS = Object.entries(SOURCE_LABELS) as [TicketSource, string][]

const SELECT_CLS =
  'bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-300 focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500/50 transition-colors w-full'

const INPUT_CLS =
  'bg-gray-900 border border-gray-700 rounded-lg px-3 py-1.5 text-sm text-gray-300 placeholder-gray-600 focus:outline-none focus:border-violet-500 focus:ring-1 focus:ring-violet-500/50 transition-colors w-full'

export default function TicketsFilters({ filters, categories, priorities, onChange, onReset }: Props) {
  function set<K extends keyof FilterState>(key: K, value: FilterState[K]) {
    onChange({ ...filters, [key]: value })
  }

  const hasActive = Object.values(filters).some(v => v !== '')

  return (
    <div className="rounded-xl border border-gray-800 bg-gray-900/60 p-4">
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
        {/* Text search */}
        <div className="relative lg:col-span-2 xl:col-span-1">
          <svg
            className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-600 pointer-events-none"
            viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}
          >
            <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
          </svg>
          <input
            type="text"
            placeholder="Szukaj po tytule lub opisie…"
            value={filters.search}
            onChange={e => set('search', e.target.value)}
            className={INPUT_CLS + ' pl-9'}
          />
        </div>

        {/* Status */}
        <select
          value={filters.status}
          onChange={e => set('status', e.target.value as TicketStatus | '')}
          className={SELECT_CLS}
        >
          <option value="">Wszystkie statusy</option>
          {STATUS_OPTIONS.map(([val, label]) => (
            <option key={val} value={val}>{label}</option>
          ))}
        </select>

        {/* Priority */}
        <select
          value={filters.priorityId}
          onChange={e => set('priorityId', e.target.value)}
          className={SELECT_CLS}
        >
          <option value="">Wszystkie priorytety</option>
          {priorities.map(p => (
            <option key={p.id} value={String(p.id)}>{p.name}</option>
          ))}
        </select>

        {/* Category */}
        <select
          value={filters.categoryId}
          onChange={e => set('categoryId', e.target.value)}
          className={SELECT_CLS}
        >
          <option value="">Wszystkie kategorie</option>
          {categories.map(c => (
            <option key={c.id} value={String(c.id)}>{c.name}</option>
          ))}
        </select>

        {/* Source */}
        <select
          value={filters.source}
          onChange={e => set('source', e.target.value as TicketSource | '')}
          className={SELECT_CLS}
        >
          <option value="">Wszystkie źródła</option>
          {SOURCE_OPTIONS.map(([val, label]) => (
            <option key={val} value={val}>{label}</option>
          ))}
        </select>

        {/* Date from */}
        <input
          type="date"
          value={filters.dateFrom}
          onChange={e => set('dateFrom', e.target.value)}
          className={SELECT_CLS}
          title="Data od"
        />

        {/* Date to */}
        <input
          type="date"
          value={filters.dateTo}
          onChange={e => set('dateTo', e.target.value)}
          className={SELECT_CLS}
          title="Data do"
        />

        {/* Reset */}
        {hasActive && (
          <button
            onClick={onReset}
            className="flex items-center justify-center gap-1.5 px-3 py-1.5 rounded-lg border border-gray-700 hover:border-violet-500/50 text-gray-400 hover:text-gray-200 text-sm transition-colors"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-4 h-4">
              <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
            </svg>
            Wyczyść filtry
          </button>
        )}
      </div>
    </div>
  )
}
