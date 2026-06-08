import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createTicket } from '../api/tickets'
import { getCategories } from '../api/categories'
import { getPriorities } from '../api/priorities'
import { useAuth } from '../auth/AuthContext'
import { useToast } from '../context/ToastContext'
import type { Category } from '../types/category'
import type { Priority } from '../types/priority'
import type { TicketCreate } from '../types/ticket'

interface Props {
  isOpen: boolean
  onClose: () => void
}

export default function NewTicketModal({ isOpen, onClose }: Props) {
  const { currentUser, role } = useAuth()
  const { showToast } = useToast()
  const navigate = useNavigate()

  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [requesterEmail, setRequesterEmail] = useState('')
  const [requesterName, setRequesterName] = useState('')
  const [categoryId, setCategoryId] = useState('')
  const [priorityId, setPriorityId] = useState('')

  const [categories, setCategories] = useState<Category[]>([])
  const [priorities, setPriorities] = useState<Priority[]>([])
  const [loadingMeta, setLoadingMeta] = useState(false)

  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const titleRef = useRef<HTMLInputElement>(null)

  // Pre-fill email and name for end_user
  useEffect(() => {
    if (isOpen) {
      if (role === 'end_user' && currentUser) {
        setRequesterEmail(currentUser.email)
        setRequesterName(currentUser.name ?? '')
      }
      // Focus title on open
      setTimeout(() => titleRef.current?.focus(), 50)
    }
  }, [isOpen, role, currentUser])

  // Fetch categories + priorities when opened
  useEffect(() => {
    if (!isOpen) return
    setLoadingMeta(true)
    Promise.all([getCategories(), getPriorities()])
      .then(([cats, pris]) => {
        setCategories(cats)
        setPriorities(pris)
      })
      .catch(() => {
        // Non-critical — selects will just be empty
      })
      .finally(() => setLoadingMeta(false))
  }, [isOpen])

  function resetForm() {
    setTitle('')
    setDescription('')
    setRequesterEmail(role === 'end_user' && currentUser ? currentUser.email : '')
    setRequesterName(role === 'end_user' && currentUser ? (currentUser.name ?? '') : '')
    setCategoryId('')
    setPriorityId('')
    setError(null)
  }

  function handleClose() {
    resetForm()
    onClose()
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)

    if (!title.trim()) { setError('Tytuł jest wymagany.'); return }
    if (!description.trim()) { setError('Opis jest wymagany.'); return }
    if (!requesterEmail.trim()) { setError('E-mail zgłaszającego jest wymagany.'); return }

    const payload: TicketCreate = {
      title: title.trim(),
      description: description.trim(),
      requester_email: requesterEmail.trim(),
      requester_name: requesterName.trim() || null,
      category_id: categoryId ? Number(categoryId) : null,
      priority_id: priorityId ? Number(priorityId) : null,
    }

    setSubmitting(true)
    try {
      const created = await createTicket(payload)
      resetForm()
      onClose()
      showToast(`Utworzono zgłoszenie #${created.id}.`, 'success')
      // Navigate to the new ticket detail
      const detailPath = role === 'end_user'
        ? `/portal/tickets/${created.id}`
        : `/tickets/${created.id}`
      navigate(detailPath)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Błąd podczas tworzenia zgłoszenia.')
    } finally {
      setSubmitting(false)
    }
  }

  // Close on backdrop click or Escape
  function handleBackdropClick(e: React.MouseEvent<HTMLDivElement>) {
    if (e.target === e.currentTarget) handleClose()
  }

  useEffect(() => {
    if (!isOpen) return
    function onKey(e: KeyboardEvent) {
      if (e.key === 'Escape') handleClose()
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [isOpen])

  if (!isOpen) return null

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4"
      onClick={handleBackdropClick}
    >
      <div className="w-full max-w-xl bg-[#1a1d27] rounded-2xl border border-white/10 shadow-2xl overflow-hidden max-h-[95dvh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-4 sm:px-6 py-4 border-b border-white/8 shrink-0">
          <h2 className="text-base font-semibold text-gray-100">Nowe zgłoszenie</h2>
          <button
            onClick={handleClose}
            className="text-gray-500 hover:text-gray-300 transition-colors p-1 rounded-md hover:bg-white/5"
            aria-label="Zamknij"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2} className="w-5 h-5">
              <line x1="18" y1="6" x2="6" y2="18" />
              <line x1="6" y1="6" x2="18" y2="18" />
            </svg>
          </button>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} noValidate className="flex flex-col flex-1 min-h-0">
          <div className="px-4 sm:px-6 py-5 space-y-4 overflow-y-auto flex-1">
            {error && (
              <div className="bg-red-500/10 border border-red-500/30 rounded-lg px-4 py-3 text-sm text-red-400">
                {error}
              </div>
            )}

            {/* Title */}
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-gray-400 block">
                Tytuł <span className="text-red-400">*</span>
              </label>
              <input
                ref={titleRef}
                type="text"
                value={title}
                onChange={e => setTitle(e.target.value)}
                maxLength={255}
                placeholder="Krótki opis problemu"
                className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2.5 focus:outline-none focus:ring-1 focus:ring-violet-500 placeholder-gray-600"
              />
            </div>

            {/* Description */}
            <div className="space-y-1.5">
              <label className="text-xs font-medium text-gray-400 block">
                Opis <span className="text-red-400">*</span>
              </label>
              <textarea
                value={description}
                onChange={e => setDescription(e.target.value)}
                rows={4}
                placeholder="Szczegółowy opis zgłoszenia…"
                className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2.5 focus:outline-none focus:ring-1 focus:ring-violet-500 placeholder-gray-600 resize-y"
              />
            </div>

            {/* Requester email + name */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-400 block">
                  E-mail zgłaszającego <span className="text-red-400">*</span>
                </label>
                <input
                  type="email"
                  value={requesterEmail}
                  onChange={e => setRequesterEmail(e.target.value)}
                  placeholder="user@firma.pl"
                  readOnly={role === 'end_user'}
                  className={`w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2.5 focus:outline-none focus:ring-1 focus:ring-violet-500 placeholder-gray-600 ${role === 'end_user' ? 'opacity-60 cursor-not-allowed' : ''}`}
                />
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-400 block">
                  Imię i nazwisko
                </label>
                <input
                  type="text"
                  value={requesterName}
                  onChange={e => setRequesterName(e.target.value)}
                  placeholder="Jan Kowalski"
                  className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2.5 focus:outline-none focus:ring-1 focus:ring-violet-500 placeholder-gray-600"
                />
              </div>
            </div>

            {/* Category + Priority */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-400 block">Kategoria</label>
                <select
                  value={categoryId}
                  onChange={e => setCategoryId(e.target.value)}
                  disabled={loadingMeta}
                  className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2.5 focus:outline-none focus:ring-1 focus:ring-violet-500 disabled:opacity-50"
                >
                  <option value="">— brak —</option>
                  {categories.map(c => (
                    <option key={c.id} value={c.id}>{c.name}</option>
                  ))}
                </select>
              </div>
              <div className="space-y-1.5">
                <label className="text-xs font-medium text-gray-400 block">Priorytet</label>
                <select
                  value={priorityId}
                  onChange={e => setPriorityId(e.target.value)}
                  disabled={loadingMeta}
                  className="w-full bg-[#0f1117] border border-white/10 rounded-lg text-sm text-gray-200 px-3 py-2.5 focus:outline-none focus:ring-1 focus:ring-violet-500 disabled:opacity-50"
                >
                  <option value="">— brak —</option>
                  {priorities.map(p => (
                    <option key={p.id} value={p.id}>{p.name}</option>
                  ))}
                </select>
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="flex items-center justify-end gap-3 px-4 sm:px-6 py-4 border-t border-white/8 bg-[#0f1117]/50 shrink-0">
            <button
              type="button"
              onClick={handleClose}
              className="text-sm text-gray-400 hover:text-gray-200 px-4 py-2 rounded-lg hover:bg-white/5 transition-colors"
            >
              Anuluj
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex items-center gap-2 bg-violet-600 hover:bg-violet-500 disabled:opacity-50 text-white text-sm font-medium px-5 py-2 rounded-lg transition-colors"
            >
              {submitting ? (
                <>
                  <svg className="animate-spin w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={2}>
                    <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83" />
                  </svg>
                  Tworzenie…
                </>
              ) : 'Utwórz zgłoszenie'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
