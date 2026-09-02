import type { Payment } from "../types";
import { formatDate, formatDateTime } from "../utils/dates";
import { PLACEHOLDER, textOrPlaceholder } from "../utils/display";
import { formatMoney } from "../utils/money";
import { StatusBadge } from "./StatusBadge";

interface PaymentsTableProps {
  payments: Payment[];
}

export function PaymentsTable({ payments }: PaymentsTableProps) {
  return (
    <table className="data-table">
      <thead>
        <tr>
          <th scope="col">Payee</th>
          <th scope="col" className="numeric">
            Amount
          </th>
          <th scope="col">Status</th>
          <th scope="col">Scheduled for</th>
          <th scope="col">Memo</th>
          <th scope="col">Created</th>
        </tr>
      </thead>
      <tbody>
        {payments.length === 0 && (
          <tr>
            <td colSpan={6} className="empty-row">
              No payments match this filter.
            </td>
          </tr>
        )}
        {payments.map((payment) => (
          <tr key={payment.processor_payment_id}>
            <td>{payment.payee_name}</td>
            <td className="numeric">{formatMoney(payment.amount, payment.currency)}</td>
            <td>
              <StatusBadge status={payment.status} />
            </td>
            <td>{payment.scheduled_for ? formatDate(payment.scheduled_for) : PLACEHOLDER}</td>
            <td className="muted">{textOrPlaceholder(payment.memo)}</td>
            <td>{formatDateTime(payment.created_at)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
