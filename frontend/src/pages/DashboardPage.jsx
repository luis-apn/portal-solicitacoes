import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'

export default function DashboardPage() {
  const [summary, setSummary] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api('/dashboard')
      .then((data) => setSummary(data))
      .catch((err) => setError(err.message))
  }, [])

  if (error) return <p className="error">{error}</p>
  if (!summary) return <p>Carregando...</p>

  return (
    <div>
      <h1>Dashboard</h1>

      <div className="cards">
        <div className="card stat">
          <span>Total de solicitações</span>
          <strong>{summary.total}</strong>
        </div>
        <div className="card stat stat-ABERTO">
          <span>Abertas</span>
          <strong>{summary.aberto}</strong>
        </div>
        <div className="card stat stat-EM_ATENDIMENTO">
          <span>Em atendimento</span>
          <strong>{summary.em_atendimento}</strong>
        </div>
        <div className="card stat stat-CONCLUIDO">
          <span>Concluídas</span>
          <strong>{summary.concluido}</strong>
        </div>
      </div>

      <Link className="btn" to="/solicitacoes">Ver solicitações</Link>
    </div>
  )
}
