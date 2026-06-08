import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './auth/AuthContext'
import { ToastProvider } from './context/ToastContext'
import ProtectedRoute from './components/ProtectedRoute'
import AppShell from './components/AppShell'
import LoginPage from './pages/LoginPage'
import NotFoundPage from './pages/NotFoundPage'
import DashboardPage from './pages/DashboardPage'
import TicketsPage from './pages/TicketsPage'
import TicketDetailsPage from './pages/TicketDetailsPage'
import KnowledgePage from './pages/KnowledgePage'
import KnowledgeArticlePage from './pages/KnowledgeArticlePage'
import AIPage from './pages/AIPage'
import SettingsPage from './pages/SettingsPage'
import PortalTicketsPage from './pages/portal/PortalTicketsPage'
import PortalTicketDetailsPage from './pages/portal/PortalTicketDetailsPage'
import PortalNewTicketPage from './pages/portal/PortalNewTicketPage'
import PortalProfilePage from './pages/portal/PortalProfilePage'
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
        <ToastProvider>
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

                    {/* Agent panel */}
                    <Route
                      path="/dashboard"
                      element={
                        <ProtectedRoute allowedRoles={['agent']} redirectTo="/portal/tickets">
                          <DashboardPage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/tickets"
                      element={
                        <ProtectedRoute allowedRoles={['agent']} redirectTo="/portal/tickets">
                          <TicketsPage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/tickets/:id"
                      element={
                        <ProtectedRoute allowedRoles={['agent']} redirectTo="/portal/tickets">
                          <TicketDetailsPage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/knowledge"
                      element={
                        <ProtectedRoute allowedRoles={['agent']} redirectTo="/portal/tickets">
                          <KnowledgePage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/knowledge/:id"
                      element={
                        <ProtectedRoute allowedRoles={['agent']} redirectTo="/portal/tickets">
                          <KnowledgeArticlePage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/ai"
                      element={
                        <ProtectedRoute allowedRoles={['agent']} redirectTo="/portal/tickets">
                          <AIPage />
                        </ProtectedRoute>
                      }
                    />
                    <Route
                      path="/settings"
                      element={
                        <ProtectedRoute allowedRoles={['agent']} redirectTo="/portal/tickets">
                          <SettingsPage />
                        </ProtectedRoute>
                      }
                    />
                    {/* Legacy quality route redirect */}
                    <Route path="/quality" element={<Navigate to="/ai" replace />} />

                    {/* End-user portal */}
                    <Route path="/portal" element={<Navigate to="/portal/tickets" replace />} />
                    <Route path="/portal/tickets" element={<PortalTicketsPage />} />
                    <Route path="/portal/tickets/:id" element={<PortalTicketDetailsPage />} />
                    <Route path="/portal/new-ticket" element={<PortalNewTicketPage />} />
                    <Route path="/portal/settings" element={<PortalProfilePage />} />
                    <Route path="/portal/profile" element={<PortalProfilePage />} />

                    {/* 404 */}
                    <Route path="*" element={<NotFoundPage />} />
                  </Routes>
                </AppShell>
              </ProtectedRoute>
            }
          />
        </Routes>
        </ToastProvider>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App

