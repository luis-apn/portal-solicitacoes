import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api } from '../api'
import { useAuth } from '../AuthContext'
import StatusBadge from '../components/StatusBadge'
import { NEXT_STATUS, formatDate } from '../utils'

export default function RequestDetailPage() {
  const { id } = useParams()
  const { user } = useAuth()
  const navigate = useNavigate()
  const [request, setRequest] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api('/requests/' + id)
      .then((data) => setRequest(data.request))
      .catch((err) => setError(err.message))
  }, [id])

  async function handleDelete() {
    if (!window.confirm('Deseja realmente excluir esta solicitação?')) return
    try {
      await api('/requests/' + id, { method: 'DELETE' })
      navigate('/solicitacoes')
    } catch (err) {
      setError(err.message)
    }
  }

  async function handleChangeStatus(newStatus) {
    setError('')
    try {
      const data = await api('/requests/' + id + '/status', { method: 'PATCH', body: { status: newStatus } })
      setRequest(data.request)
    } catch (err) {
      setError(err.message)
    }
  }

  if (!request) {
    return error ? <p className="error">{error}</p> : <p>Carregando...</p>
  }

  // Os botões aparecem só para quem pode usar. O backend valida de novo de qualquer forma.
  const isOwner = request.requester_id === user.id
  const canEdit = isOwner && request.status === 'ABERTO'
  const next = NEXT_STATUS[request.status]
  const canChangeStatus = user.role === 'ATENDENTE' && next

  return (
    <div>
      <div className="page-header">
        <h1>Solicitação #{request.id}</h1>
        <Link to="/solicitacoes">Voltar para a lista</Link>
      </div>

      <div className="card">
        <h2>{request.title}</h2>
        <dl className="details">
          <dt>Status</dt>
          <dd><StatusBadge status={request.status} /></dd>
          <dt>Categoria</dt>
          <dd>{request.category}</dd>
          <dt>Solicitante</dt>
          <dd>{request.requester}</dd>
          <dt>Aberta em</dt>
          <dd>{formatDate(request.created_at)}</dd>
          <dt>Última atualização</dt>
          <dd>{formatDate(request.updated_at)}</dd>
        </dl>
        <h3>Descrição</h3>
        <p className="description">{request.description}</p>

        {error && <p className="error">{error}</p>}

        <div className="actions">
          {canChangeStatus && (
            <button className="btn" onClick={() => handleChangeStatus(next.status)}>{next.label}</button>
          )}
          {canEdit && (
            <>
              <Link className="btn btn-secondary" to={'/solicitacoes/' + request.id + '/editar'}>Editar</Link>
              <button className="btn btn-danger" onClick={handleDelete}>Excluir</button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
