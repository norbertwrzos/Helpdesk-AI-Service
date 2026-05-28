import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './auth/AuthContext'
import ProtectedRoute from './components/ProtectedRoute'
import Layout from './components/Layout'
import LoginPage from './pages/LoginPage'
import HomePage from './pages/HomePage'
import TicketsPage from './pages/TicketsPage'
import TicketDetailsPage from './pages/TicketDetailsPage'
import EmailImportPage from './pages/EmailImportPage'
import QualityPage from './pages/QualityPage'
import UserPortalPage from './pages/UserPortalPage'
import './App.css'

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />

          {/* Portal użytkownika końcowego */}
          <Route
            path="/portal"
            element={
              <ProtectedRoute allowedRoles={['end_user']} redirectTo="/">
                <UserPortalPage />
              </ProtectedRoute>
            }
          />

          {/* Główny panel — admin i agent */}
          <Route
            path="/*"
            element={
              <ProtectedRoute allowedRoles={['admin', 'agent']} redirectTo="/portal">
                <Layout>
                  <Routes>
                    <Route path="/" element={<HomePage />} />
                    <Route path="/tickets" element={<TicketsPage />} />
                    <Route path="/tickets/:id" element={<TicketDetailsPage />} />
                    <Route path="/email-import" element={<EmailImportPage />} />
                    <Route path="/quality" element={<QualityPage />} />
                    <Route path="*" element={<Navigate to="/" replace />} />
                  </Routes>
                </Layout>
              </ProtectedRoute>
            }
          />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App

