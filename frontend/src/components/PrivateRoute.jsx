import { Navigate, Outlet } from 'react-router-dom'
import { useAuth } from '../AuthContext'
import Navbar from './Navbar'

// Protege as páginas internas: sem login, manda para /login.
export default function PrivateRoute() {
  const { user, loading } = useAuth()

  if (loading) {
    return <p className="container">Carregando...</p>
  }

  if (!user) {
    return <Navigate to="/login" replace />
  }

  return (
    <>
      <Navbar />
      <main className="container">
        <Outlet />
      </main>
    </>
  )
}
