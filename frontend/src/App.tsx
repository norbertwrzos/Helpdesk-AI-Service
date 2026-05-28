import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import HomePage from './pages/HomePage'
import TicketsPage from './pages/TicketsPage'
import TicketDetailsPage from './pages/TicketDetailsPage'
import EmailImportPage from './pages/EmailImportPage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/tickets" element={<TicketsPage />} />
          <Route path="/tickets/:id" element={<TicketDetailsPage />} />
          <Route path="/email-import" element={<EmailImportPage />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App

