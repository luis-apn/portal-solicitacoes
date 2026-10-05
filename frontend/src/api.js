// Função única para chamar a API. Todas as telas usam ela.
// - envia e recebe JSON
// - envia o cookie de sessão (credentials: 'include')
// - se a API responder com erro, lança um Error com a mensagem vinda do backend
export async function api(path, options = {}) {
  const response = await fetch('/api' + path, {
    method: options.method || 'GET',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: options.body ? JSON.stringify(options.body) : undefined,
  })

  let data = null
  try {
    data = await response.json()
  } catch {
    data = null
  }

  if (!response.ok) {
    // Sessão expirou durante o uso: volta para o login.
    if (response.status === 401 && !path.startsWith('/auth/')) {
      window.location.href = '/login'
    }

    const error = new Error((data && data.error) || 'Erro ao comunicar com o servidor.')
    error.status = response.status
    error.details = (data && data.details) || {}
    throw error
  }

  return data
}
