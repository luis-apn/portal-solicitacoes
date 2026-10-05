import { createContext, useContext, useEffect, useState } from 'react'
import { api } from './api'

// Contexto guarda o usuário logado e deixa disponível para qualquer componente.
const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  // Ao abrir o site, pergunta ao backend se já existe uma sessão ativa.
  useEffect(() => {
    api('/auth/me')
      .then((data) => setUser(data.user))
      .catch(() => setUser(null))
      .finally(() => setLoading(false))
  }, [])

  async function login(username, password) {
    const data = await api('/auth/login', { method: 'POST', body: { username, password } })
    setUser(data.user)
  }

  async function logout() {
    try {
      await api('/auth/logout', { method: 'POST' })
    } finally {
      setUser(null)
    }
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  return useContext(AuthContext)
}
