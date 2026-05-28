import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import AppShell from './components/AppShell'
import LoginPage from './pages/LoginPage'
import DashboardPage from './pages/DashboardPage'
import TicketsPage from './pages/TicketsPage'
import TicketDetailsPage from './pages/TicketDetailsPage'
import EmailImportPage from './pages/EmailImportPage'
import KnowledgePage from './pages/KnowledgePage'
import AIPage from './pages/AIPage'
import SettingsPage from './pages/SettingsPage'
import PortalTicketsPage from './pages/portal/PortalTicketsPage'
import PortalTicketDetailsPage from './pages/portal/PortalTicketDetailsPage'
import './App.css'

/** Redirect / based on role */
function HomeRedirect() {
  const { role } = useAuth()
  if (role === 'end_user') return <Navigate to="/portal/tickets" replace />
  return <Navigate to="/dashboard" replace />
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public */}
          <Route path="/login" element={<LoginPage />} />

          {/* All authenticated users → AppShell */}
          <Route
            path="/*"
            element={
              <ProtectedRoute>
                <AppShell>
                  <Routes>
                    <Route path="/" element={<HomeRedirect />} />

                    {/* Admin / Agent panel */}
                    <Route path="/dashboard" element={<DashboardPage />} />
                    <Route path="/tickets" element={<TicketsPage />} />
                    <Route path="/tickets/:id" element={<TicketDetailsPage />} />
                    <Route path="/knowledge" element={<KnowledgePage />} />
                    <Route path="/ai" element={<AIPage />} />
                    <Route path="/settings" element={<SettingsPage />} />
                    {/* Keep old route for backward compatibility */}
                    <Route path="/quality" element={<AIPage />} />
                    <Route path="/email-import" element={<EmailImportPage />} />

                    {/* End-user portal */}
                    <Route path="/portal" element={<Navigate to="/portal/tickets" replace />} />
                    <Route path="/portal/tickets" element={<PortalTicketsPage />} />
                    <Route path="/portal/tickets/:id" element={<PortalTicketDetailsPage />} />

                    {/* Fallback */}
                    <Route path="*" element={<HomeRedirect />} />
                  </Routes>
                </AppShell>
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App

