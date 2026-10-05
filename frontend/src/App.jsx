import { Navigate, Route, Routes } from 'react-router-dom'
import PrivateRoute from './components/PrivateRoute'
import DashboardPage from './pages/DashboardPage'
import LoginPage from './pages/LoginPage'
import RequestDetailPage from './pages/RequestDetailPage'
import RequestFormPage from './pages/RequestFormPage'
import RequestListPage from './pages/RequestListPage'

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />

      {/* Todas as rotas abaixo exigem login */}
      <Route element={<PrivateRoute />}>
        <Route path="/" element={<DashboardPage />} />
        <Route path="/solicitacoes" element={<RequestListPage />} />
        <Route path="/solicitacoes/nova" element={<RequestFormPage />} />
        <Route path="/solicitacoes/:id" element={<RequestDetailPage />} />
        <Route path="/solicitacoes/:id/editar" element={<RequestFormPage />} />
      </Route>

      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}
