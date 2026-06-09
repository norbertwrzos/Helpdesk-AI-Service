import { useState } from 'react'
import type { Ticket, TicketStatus, TicketUpdate } from '../types/ticket'
import { TICKET_STATUS_LABELS } from '../types/ticket'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import { formatDateTime } from '../utils/dateFormat'

interface Props {
  ticket: Ticket
  categories: Category[]
  priorities: Priority[]
  onUpdate: (update: TicketUpdate) => Promise<void>
}

const STATUS_OPTIONS = (Object.entries(TICKET_STATUS_LABELS) as [TicketStatus, string][]).map(
  ([value, label]) => ({ value, label }),
)

export default function TicketPropertiesPanel({ ticket, categories, priorities, onUpdate }: Props) {
  const [status, setStatus] = useState<TicketStatus>(ticket.status)
  const [categoryId, setCategoryId] = useState<string>(ticket.category_id?.toString() ?? '')
  const [priorityId, setPriorityId] = useState<string>(ticket.priority_id?.toString() ?? '')
  const [agentName, setAgentName] = useState<string>(ticket.assigned_agent_name ?? '')
  const [saving, setSaving] = useState(false)
  const [saveError, setSaveError] = useState<string | null>(null)
  const [saveSuccess, setSaveSuccess] = useState(false)

  async function handleSave() {
    setSaveError(null)
    setSaveSuccess(false)
    setSaving(true)
    try {
      await onUpdate({
        status,
        category_id: categoryId ? Number(categoryId) : null,
        priority_id: priorityId ? Number(priorityId) : null,
        assigned_agent_name: agentName.trim() || undefined,
      })
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : 'Błąd podczas zapisywania.')
    } finally {
      setSaving(false)
    }
  }

  async function handleResolve() {
    setSaveError(null)
    setSaveSuccess(false)
    setSaving(true)
    try {
      setStatus('resolved')
      await onUpdate({ status: 'resolved' })
      setSaveSuccess(true)
      setTimeout(() => setSaveSuccess(false), 3000)
    } catch (err) {
      setSaveError(err instanceof Error ? err.message : 'Błąd podczas rozwiązywania.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <aside className="bg-surface rounded-xl border border-white/8 p-5 space-y-5 sticky top-6">
      <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-wider">Właściwości</h2>

      {/* Status */}
      <div className="space-y-1.5">
        <label className="text-xs text-gray-500 font-medium block">Status</label>
        
        <select
          className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-violet-500"
          value={status}
          onChange={e => setStatus(e.target.value as TicketStatus)}
        >
          {STATUS_OPTIONS.map(o => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>

      {/* Category */}
      <div className="space-y-1.5">
        <label className="text-xs text-gray-500 font-medium block">Kategoria</label>
        <select
          className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-violet-500"
          value={categoryId}
          onChange={e => setCategoryId(e.target.value)}
        >
          <option value="">— brak —</option>
          {categories.map(c => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
      </div>

      {/* Priority */}
      <div className="space-y-1.5">
        <label className="text-xs text-gray-500 font-medium block">Priorytet</label>
        <select
          className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-violet-500"
          value={priorityId}
          onChange={e => setPriorityId(e.target.value)}
        >
          <option value="">— brak —</option>
          {priorities.map(p => (
            <option key={p.id} value={p.id}>{p.name}</option>
          ))}
        </select>
      </div>

      {/* Agent */}
      <div className="space-y-1.5">
        <label className="text-xs text-gray-500 font-medium block">Przypisany agent</label>
        <input
          type="text"
          className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2 focus:outline-none focus:ring-1 focus:ring-violet-500"
          value={agentName}
          onChange={e => setAgentName(e.target.value)}
          placeholder="Nie przypisano"
        />
      </div>

      

      {/* Readonly info */}
      <div className="space-y-3">
        

        

        <div className="flex justify-between items-center gap-2">
          <span className="text-xs text-gray-500">Utworzono</span>
          <span className="text-xs text-gray-400">{formatDateTime(ticket.created_at)}</span>
        </div>

        <div className="flex justify-between items-center gap-2">
          <span className="text-xs text-gray-500">Zaktualizowano</span>
          <span className="text-xs text-gray-400">{formatDateTime(ticket.updated_at)}</span>
        </div>
      </div>

      {/* Actions */}
      {saveError && (
        <p className="text-xs text-red-400">{saveError}</p>
      )}
      {saveSuccess && (
        <p className="text-xs text-green-400">Zmiany zapisane.</p>
      )}

      <div className="space-y-2">
        <button
          className="w-full bg-green-600 hover:bg-green-500 disabled:opacity-50 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          onClick={handleResolve}
          disabled={saving || status === 'resolved'}
        >
          ✓ Rozwiąż zgłoszenie
        </button>
        <button
          className="w-full bg-violet-600 hover:bg-violet-500 disabled:opacity-50 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
          onClick={handleSave}
          disabled={saving}
        >
          {saving ? 'Zapisywanie…' : 'Zapisz zmiany'}
        </button>
      </div>
    </aside>
  )
}
