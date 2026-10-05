export const STATUS_LABELS = {
  ABERTO: 'Aberto',
  EM_ATENDIMENTO: 'Em Atendimento',
  CONCLUIDO: 'Concluído',
}

// Próximo status permitido e o texto do botão (mesma regra do backend).
export const NEXT_STATUS = {
  ABERTO: { status: 'EM_ATENDIMENTO', label: 'Iniciar atendimento' },
  EM_ATENDIMENTO: { status: 'CONCLUIDO', label: 'Concluir' },
}

export function formatDate(isoDate) {
  return new Date(isoDate).toLocaleString('pt-BR', {
    dateStyle: 'short',
    timeStyle: 'short',
  })
}
