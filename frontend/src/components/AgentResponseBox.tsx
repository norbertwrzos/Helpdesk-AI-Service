import { useState } from 'react'
import { updateTicket } from '../api/tickets'

interface Props {
  ticketId: number
  initialResponse: string | null | undefined
  onSaved: (response: string) => void
}

export default function AgentResponseBox({ ticketId, initialResponse, onSaved }: Props) {
  const [response, setResponse] = useState<string>(initialResponse ?? '')
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  async function handleSave() {
    setError(null)
    setSuccess(false)
    setSaving(true)
    try {
      const updated = await updateTicket(ticketId, { agent_response: response.trim() || undefined })
      setSuccess(true)
      onSaved(updated.agent_response ?? '')
      setTimeout(() => setSuccess(false), 3000)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd podczas zapisywania odpowiedzi.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="bg-surface rounded-xl border border-white/8 p-5 space-y-3">
      <h3 className="text-sm font-semibold text-gray-300">Odpowiedź agenta</h3>
      <textarea
        className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2.5 focus:outline-none focus:ring-1 focus:ring-violet-500 resize-y min-h-[100px]"
        value={response}
        onChange={e => setResponse(e.target.value)}
        placeholder="Wpisz odpowiedź dla zgłaszającego…"
        rows={4}
      />
      {error && <p className="text-xs text-red-400">{error}</p>}
      {success && <p className="text-xs text-green-400">Odpowiedź zapisana.</p>}
      <button
        className="bg-violet-600 hover:bg-violet-500 disabled:opacity-50 text-white text-sm font-medium px-4 py-2 rounded-lg transition-colors"
        onClick={handleSave}
        disabled={saving}
      >
        {saving ? 'Zapisywanie…' : 'Zapisz odpowiedź agenta'}
      </button>
    </div>
  )
}
