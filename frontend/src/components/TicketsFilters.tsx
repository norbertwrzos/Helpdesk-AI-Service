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

const LABEL_CLS =
  'mb-2 block text-[11px] font-semibold uppercase tracking-[0.14em] text-gray-500'

const SELECT_CLS =
  'h-12 w-full appearance-none rounded-xl border border-white/10 bg-slate-950/75 px-4 pr-10 text-sm text-gray-100 shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] transition-all focus:border-violet-400/50 focus:outline-none focus:ring-2 focus:ring-violet-500/20'

const INPUT_CLS =
  'h-12 w-full rounded-xl border border-white/10 bg-slate-950/75 px-4 text-sm text-gray-100 placeholder:text-gray-500 shadow-[inset_0_1px_0_rgba(255,255,255,0.03)] transition-all focus:border-violet-400/50 focus:outline-none focus:ring-2 focus:ring-violet-500/20'

export default function TicketsFilters({ filters, categories, priorities, onChange, onReset }: Props) {
  function set<K extends keyof FilterState>(key: K, value: FilterState[K]) {
    onChange({ ...filters, [key]: value })
  }

  const hasActive = Object.values(filters).some(v => v !== '')

  return (
    <div className="surface-card surface-card--padded">
      <div className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-12">
        {/* Text search */}
        <div className="md:col-span-2 xl:col-span-4">
          <label className={LABEL_CLS} htmlFor="tickets-search">Szukaj</label>
          <div className="relative">
            <span className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-4 text-gray-500">
              <svg
                className="h-4 w-4"
                viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}
              >
                <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
              </svg>
            </span>
            <input
              id="tickets-search"
              type="text"
              placeholder="Szukaj po tytule lub opisie…"
              value={filters.search}
              onChange={e => set('search', e.target.value)}
              className={INPUT_CLS + ' pl-11'}
            />
          </div>
        </div>

        {/* Status */}
        <div className="xl:col-span-2">
          <label className={LABEL_CLS} htmlFor="tickets-status">Status</label>
          <div className="relative">
            <select
              id="tickets-status"
              value={filters.status}
              onChange={e => set('status', e.target.value as TicketStatus | '')}
              className={SELECT_CLS}
            >
              <option value="">Wszystkie statusy</option>
              {STATUS_OPTIONS.map(([val, label]) => (
                <option key={val} value={val}>{label}</option>
              ))}
            </select>
            <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-500">
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </span>
          </div>
        </div>

        {/* Priority */}
        <div className="xl:col-span-2">
          <label className={LABEL_CLS} htmlFor="tickets-priority">Priorytet</label>
          <div className="relative">
            <select
              id="tickets-priority"
              value={filters.priorityId}
              onChange={e => set('priorityId', e.target.value)}
              className={SELECT_CLS}
            >
              <option value="">Wszystkie priorytety</option>
              {priorities.map(p => (
                <option key={p.id} value={String(p.id)}>{p.name}</option>
              ))}
            </select>
            <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-500">
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </span>
          </div>
        </div>

        {/* Category */}
        <div className="xl:col-span-2">
          <label className={LABEL_CLS} htmlFor="tickets-category">Kategoria</label>
          <div className="relative">
            <select
              id="tickets-category"
              value={filters.categoryId}
              onChange={e => set('categoryId', e.target.value)}
              className={SELECT_CLS}
            >
              <option value="">Wszystkie kategorie</option>
              {categories.map(c => (
                <option key={c.id} value={String(c.id)}>{c.name}</option>
              ))}
            </select>
            <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-500">
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </span>
          </div>
        </div>

        {/* Source */}
        <div className="xl:col-span-2">
          <label className={LABEL_CLS} htmlFor="tickets-source">Źródło</label>
          <div className="relative">
            <select
              id="tickets-source"
              value={filters.source}
              onChange={e => set('source', e.target.value as TicketSource | '')}
              className={SELECT_CLS}
            >
              <option value="">Wszystkie źródła</option>
              {SOURCE_OPTIONS.map(([val, label]) => (
                <option key={val} value={val}>{label}</option>
              ))}
            </select>
            <span className="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-4 text-gray-500">
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                <polyline points="6 9 12 15 18 9" />
              </svg>
            </span>
          </div>
        </div>

        {/* Date from */}
        <div className="xl:col-span-2">
          <label className={LABEL_CLS} htmlFor="tickets-date-from">Data od</label>
          <input
            id="tickets-date-from"
            type="date"
            value={filters.dateFrom}
            onChange={e => set('dateFrom', e.target.value)}
            className={INPUT_CLS + ' [color-scheme:dark]'}
            title="Data od"
          />
        </div>

        {/* Date to */}
        <div className="xl:col-span-2">
          <label className={LABEL_CLS} htmlFor="tickets-date-to">Data do</label>
          <input
            id="tickets-date-to"
            type="date"
            value={filters.dateTo}
            onChange={e => set('dateTo', e.target.value)}
            className={INPUT_CLS + ' [color-scheme:dark]'}
            title="Data do"
          />
        </div>

        {/* Reset */}
        {hasActive && (
          <div className="flex items-end xl:col-span-2">
            <button
              onClick={onReset}
              className="inline-flex h-12 w-full items-center justify-center gap-2 rounded-xl border border-white/10 bg-white/[0.03] px-4 text-sm font-medium text-slate-300 transition-all hover:border-violet-400/30 hover:bg-white/[0.06] hover:text-white"
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="h-4 w-4">
                <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
              </svg>
              Wyczyść filtry
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
