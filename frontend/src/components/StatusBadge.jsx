import { STATUS_LABELS } from '../utils'

export default function StatusBadge({ status }) {
  return <span className={'badge badge-' + status}>{STATUS_LABELS[status]}</span>
}
