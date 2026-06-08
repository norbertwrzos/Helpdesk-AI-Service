import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import NewTicketModal from '../../components/NewTicketModal'
import PortalLayout from '../../components/PortalLayout'

export default function PortalNewTicketPage() {
  const navigate = useNavigate()
  const [modalOpen, setModalOpen] = useState(true)

  function handleClose() {
    setModalOpen(false)
    navigate('/portal/tickets')
  }

  return (
    <PortalLayout>
      <div className="page">
        <div className="page__header">
          <h1 className="page__title">Nowe zgłoszenie</h1>
          <p className="page__subtitle">Wypełnij formularz, aby zgłosić problem techniczny.</p>
        </div>
      </div>
      <NewTicketModal isOpen={modalOpen} onClose={handleClose} />
    </PortalLayout>
  )
}
