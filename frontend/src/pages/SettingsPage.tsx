import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import SettingsTabs, { type TabKey } from '../components/settings/SettingsTabs'
import CategoriesSettings from '../components/settings/CategoriesSettings'
import PrioritiesSettings from '../components/settings/PrioritiesSettings'
import MockUserSettings from '../components/settings/MockUserSettings'
import SupportEmailSettingsInfo from '../components/settings/SupportEmailSettingsInfo'

export default function SettingsPage() {
  const { currentUser, role, logout } = useAuth()
  const navigate = useNavigate()
  const isAdmin = role === 'admin'
  const [activeTab, setActiveTab] = useState<TabKey>('categories')

  if (!currentUser) return null

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div className="page">
      <div className="page__header">
        <h1 className="page__title">Ustawienia</h1>
        <p className="page__subtitle">
          {isAdmin
            ? 'Zarządzanie konfiguracją systemu.'
            : 'Widok konfiguracji systemu (tylko odczyt).'}
        </p>
      </div>

      <div className="mt-6">
        <SettingsTabs active={activeTab} onChange={setActiveTab} />

        {activeTab === 'categories' && <CategoriesSettings isAdmin={isAdmin} />}
        {activeTab === 'priorities' && <PrioritiesSettings isAdmin={isAdmin} />}
        {activeTab === 'profile'    && <MockUserSettings user={currentUser} onLogout={handleLogout} />}
        {activeTab === 'email'      && <SupportEmailSettingsInfo />}
      </div>
    </div>
  )
}
