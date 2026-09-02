import type { KeyboardEvent } from "react";
import type { Invoice } from "../types";
import { formatDate } from "../utils/dates";
import { PLACEHOLDER, textOrPlaceholder } from "../utils/display";
import { formatMoney } from "../utils/money";
import { StatusBadge } from "./StatusBadge";

interface InvoicesTableProps {
  invoices: Invoice[];
  selectedInvoiceId: number | null;
  onSelectInvoice: (invoiceId: number) => void;
}

export function InvoicesTable({ invoices, selectedInvoiceId, onSelectInvoice }: InvoicesTableProps) {
  function handleRowKeyDown(event: KeyboardEvent<HTMLTableRowElement>, invoiceId: number) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onSelectInvoice(invoiceId);
    }
  }

  return (
    <table className="data-table">
      <thead>
        <tr>
          <th scope="col">File</th>
          <th scope="col">Vendor</th>
          <th scope="col">Invoice #</th>
          <th scope="col" className="numeric">
            Total
          </th>
          <th scope="col">Due</th>
          <th scope="col">Status</th>
          <th scope="col">Payee</th>
        </tr>
      </thead>
      <tbody>
        {invoices.length === 0 && (
          <tr>
            <td colSpan={7} className="empty-row">
              No invoices uploaded yet.
            </td>
          </tr>
        )}
        {invoices.map((invoice) => (
          <tr
            key={invoice.id}
            className="selectable-row"
            tabIndex={0}
            aria-selected={invoice.id === selectedInvoiceId}
            onClick={() => onSelectInvoice(invoice.id)}
            onKeyDown={(event) => handleRowKeyDown(event, invoice.id)}
          >
            <td>{invoice.source_filename}</td>
            <td>{textOrPlaceholder(invoice.vendor_name)}</td>
            <td>{textOrPlaceholder(invoice.invoice_number)}</td>
            <td className="numeric">
              {invoice.total_amount ? formatMoney(invoice.total_amount, invoice.currency) : PLACEHOLDER}
            </td>
            <td>{invoice.due_date ? formatDate(invoice.due_date) : PLACEHOLDER}</td>
            <td>
              <StatusBadge status={invoice.status} />
            </td>
            <td>{textOrPlaceholder(invoice.payee_name)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
