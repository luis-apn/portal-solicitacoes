import { useEffect, useState } from 'react'
import { Link, useNavigate, useParams } from 'react-router-dom'
import { api } from '../api'

// A mesma página serve para criar (/solicitacoes/nova) e editar (/solicitacoes/:id/editar).
export default function RequestFormPage() {
  const { id } = useParams()
  const isEditing = Boolean(id)
  const navigate = useNavigate()

  const [form, setForm] = useState({ title: '', description: '', category_id: '' })
  const [categories, setCategories] = useState([])
  const [error, setError] = useState('')
  const [fieldErrors, setFieldErrors] = useState({})
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    api('/categories').then((data) => setCategories(data.items))

    if (isEditing) {
      api('/requests/' + id)
        .then((data) => {
          setForm({
            title: data.request.title,
            description: data.request.description,
            category_id: String(data.request.category_id),
          })
        })
        .catch((err) => setError(err.message))
    }
  }, [id, isEditing])

  function handleChange(event) {
    setForm({ ...form, [event.target.name]: event.target.value })
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setError('')
    setFieldErrors({})
    setSubmitting(true)

    const body = { ...form, category_id: Number(form.category_id) || null }

    try {
      const data = isEditing
        ? await api('/requests/' + id, { method: 'PUT', body })
        : await api('/requests', { method: 'POST', body })
      navigate('/solicitacoes/' + data.request.id)
    } catch (err) {
      setError(err.message)
      setFieldErrors(err.details || {})
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div>
      <h1>{isEditing ? 'Editar solicitação #' + id : 'Nova solicitação'}</h1>

      <form className="card form" onSubmit={handleSubmit}>
        <label>
          Título
          <input name="title" value={form.title} onChange={handleChange} maxLength={150} required />
          {fieldErrors.title && <small className="error">{fieldErrors.title}</small>}
        </label>

        <label>
          Categoria
          <select name="category_id" value={form.category_id} onChange={handleChange} required>
            <option value="">Selecione...</option>
            {categories.map((category) => (
              <option key={category.id} value={category.id}>{category.name}</option>
            ))}
          </select>
          {fieldErrors.category_id && <small className="error">{fieldErrors.category_id}</small>}
        </label>

        <label>
          Descrição
          <textarea name="description" value={form.description} onChange={handleChange} rows={6} required />
          {fieldErrors.description && <small className="error">{fieldErrors.description}</small>}
        </label>

        {error && <p className="error">{error}</p>}

        <div className="actions">
          <button className="btn" type="submit" disabled={submitting}>
            {submitting ? 'Salvando...' : 'Salvar'}
          </button>
          <Link className="btn btn-secondary" to={isEditing ? '/solicitacoes/' + id : '/solicitacoes'}>
            Cancelar
          </Link>
        </div>
      </form>
    </div>
  )
}
