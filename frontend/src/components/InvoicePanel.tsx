import { useState } from "react";
import type { Invoice, InvoiceDecision } from "../types";
import { formatDate, formatDateTime } from "../utils/dates";
import { PLACEHOLDER, textOrPlaceholder } from "../utils/display";
import { describeError } from "../utils/errors";
import { formatMoney } from "../utils/money";
import { ErrorMessage } from "./ErrorMessage";
import { StatusBadge } from "./StatusBadge";

interface InvoicePanelProps {
  invoice: Invoice;
  onDecide: (decision: InvoiceDecision) => Promise<void>;
  onClose: () => void;
}

export function InvoicePanel({ invoice, onDecide, onClose }: InvoicePanelProps) {
  const [submittingDecision, setSubmittingDecision] = useState<InvoiceDecision | null>(null);
  const [decisionError, setDecisionError] = useState<string | null>(null);

  const canDecide = invoice.status === "needs_review" && submittingDecision === null;
  const extractedFields = [
    { label: "File", value: invoice.source_filename },
    { label: "Vendor", value: textOrPlaceholder(invoice.vendor_name) },
    { label: "Invoice #", value: textOrPlaceholder(invoice.invoice_number) },
    {
      label: "Total",
      value: invoice.total_amount ? formatMoney(invoice.total_amount, invoice.currency) : PLACEHOLDER,
    },
    { label: "Due", value: invoice.due_date ? formatDate(invoice.due_date) : PLACEHOLDER },
    { label: "Payee", value: textOrPlaceholder(invoice.payee_name) },
    { label: "Uploaded", value: formatDateTime(invoice.created_at) },
  ];

  async function submitDecision(decision: InvoiceDecision) {
    setSubmittingDecision(decision);
    setDecisionError(null);
    try {
      await onDecide(decision);
    } catch (reason) {
      setDecisionError(describeError(reason));
    } finally {
      setSubmittingDecision(null);
    }
  }

  return (
    <aside className="invoice-panel" aria-labelledby="invoice-panel-title">
      <div className="panel-header">
        <h2 id="invoice-panel-title">{invoice.vendor_name || invoice.source_filename}</h2>
        <button type="button" className="button" onClick={onClose}>
          Close
        </button>
      </div>
      <StatusBadge status={invoice.status} />

      <dl className="field-list">
        {extractedFields.map((field) => (
          <div key={field.label} className="field-row">
            <dt>{field.label}</dt>
            <dd>{field.value}</dd>
          </div>
        ))}
      </dl>

      <h3>Line items</h3>
      <table className="data-table">
        <thead>
          <tr>
            <th scope="col">Description</th>
            <th scope="col" className="numeric">
              Amount
            </th>
          </tr>
        </thead>
        <tbody>
          {invoice.line_items.length === 0 && (
            <tr>
              <td colSpan={2} className="empty-row">
                No line items extracted.
              </td>
            </tr>
          )}
          {invoice.line_items.map((lineItem, index) => (
            <tr key={`${index}-${lineItem.description}`}>
              <td>{lineItem.description}</td>
              <td className="numeric">{formatMoney(lineItem.amount, invoice.currency)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {invoice.extraction_error && (
        <div className="extraction-error">
          <h3>Extraction error</h3>
          <p>{invoice.extraction_error}</p>
        </div>
      )}

      <details className="source-document">
        <summary>Original invoice text</summary>
        <pre>{invoice.document_text}</pre>
      </details>

      {decisionError && <ErrorMessage message={decisionError} />}

      <div className="panel-actions">
        <button
          type="button"
          className="button button-primary"
          disabled={!canDecide}
          onClick={() => submitDecision("approve")}
        >
          {submittingDecision === "approve" ? "Approving" : "Approve"}
        </button>
        <button
          type="button"
          className="button button-danger"
          disabled={!canDecide}
          onClick={() => submitDecision("reject")}
        >
          {submittingDecision === "reject" ? "Rejecting" : "Reject"}
        </button>
      </div>
    </aside>
  );
}
