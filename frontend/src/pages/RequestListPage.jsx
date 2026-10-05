import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../api'
import StatusBadge from '../components/StatusBadge'
import { STATUS_LABELS, formatDate } from '../utils'

const EMPTY_FILTERS = { q: '', category_id: '', status: '', date_from: '', date_to: '' }

export default function RequestListPage() {
  const [requests, setRequests] = useState([])
  const [categories, setCategories] = useState([])
  const [filters, setFilters] = useState(EMPTY_FILTERS)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  async function loadRequests(currentFilters) {
    setLoading(true)
    setError('')

    // Monta a URL só com os filtros preenchidos. Ex: ?status=ABERTO&q=mouse
    const params = new URLSearchParams()
    Object.entries(currentFilters).forEach(([key, value]) => {
      if (value) params.append(key, value)
    })

    try {
      const data = await api('/requests?' + params.toString())
      setRequests(data.items)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    api('/categories').then((data) => setCategories(data.items))
    loadRequests(EMPTY_FILTERS)
  }, [])

  function handleChange(event) {
    setFilters({ ...filters, [event.target.name]: event.target.value })
  }

  function handleSubmit(event) {
    event.preventDefault()
    loadRequests(filters)
  }

  function handleClear() {
    setFilters(EMPTY_FILTERS)
    loadRequests(EMPTY_FILTERS)
  }

  return (
    <div>
      <div className="page-header">
        <h1>Solicitações</h1>
        <Link className="btn" to="/solicitacoes/nova">Nova solicitação</Link>
      </div>

      <form className="card filters" onSubmit={handleSubmit}>
        <label>
          Título
          <input name="q" value={filters.q} onChange={handleChange} placeholder="Buscar pelo título" />
        </label>
        <label>
          Categoria
          <select name="category_id" value={filters.category_id} onChange={handleChange}>
            <option value="">Todas</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
        </label>
        <label>
          Status
          <select name="status" value={filters.status} onChange={handleChange}>
            <option value="">Todos</option>
            {Object.entries(STATUS_LABELS).map(([value, label]) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </select>
        </label>
        <label>
          De
          <input type="date" name="date_from" value={filters.date_from} onChange={handleChange} />
        </label>
        <label>
          Até
          <input type="date" name="date_to" value={filters.date_to} onChange={handleChange} />
        </label>
        <div className="filter-buttons">
          <button className="btn" type="submit">Filtrar</button>
          <button className="btn btn-secondary" type="button" onClick={handleClear}>Limpar</button>
        </div>
      </form>

      {error && <p className="error">{error}</p>}

      {loading ? (
        <p>Carregando...</p>
      ) : requests.length === 0 ? (
        <p>Nenhuma solicitação encontrada.</p>
      ) : (
        <div className="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Código</th>
                <th>Título</th>
                <th>Categoria</th>
                <th>Solicitante</th>
                <th>Data de abertura</th>
                <th>Status</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {requests.map((item) => (
                <tr key={item.id}>
                  <td>#{item.id}</td>
                  <td>{item.title}</td>
                  <td>{item.category}</td>
                  <td>{item.requester}</td>
                  <td>{formatDate(item.created_at)}</td>
                  <td><StatusBadge status={item.status} /></td>
                  <td><Link to={'/solicitacoes/' + item.id}>Detalhes</Link></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
