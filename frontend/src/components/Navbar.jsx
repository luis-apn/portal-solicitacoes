import { NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../AuthContext'

export default function Navbar() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  async function handleLogout() {
    await logout()
    navigate('/login')
  }

  return (
    <header className="navbar">
      <strong className="navbar-title">Portal de Solicitações</strong>
      <nav className="navbar-links">
        <NavLink to="/" end>Dashboard</NavLink>
        <NavLink to="/solicitacoes" end>Solicitações</NavLink>
        <NavLink to="/solicitacoes/nova">Nova solicitação</NavLink>
      </nav>
      <div className="navbar-user">
        <span>
          {user.full_name} ({user.role === 'ATENDENTE' ? 'Atendente' : 'Solicitante'})
        </span>
        <button className="btn btn-secondary" onClick={handleLogout}>Sair</button>
      </div>
    </header>
  )
}
