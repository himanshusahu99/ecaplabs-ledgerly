import { useState } from "react";
import { decideInvoice, uploadInvoice } from "../api/invoices";
import { useInvoices } from "../hooks/useInvoices";
import type { InvoiceDecision } from "../types";
import { describeError } from "../utils/errors";
import { ErrorMessage } from "./ErrorMessage";
import { InvoicePanel } from "./InvoicePanel";
import { InvoicesTable } from "./InvoicesTable";
import { UploadButton } from "./UploadButton";

interface InvoicesTabProps {
  businessId: string;
}

export function InvoicesTab({ businessId }: InvoicesTabProps) {
  const invoices = useInvoices(businessId);
  const [selectedInvoiceId, setSelectedInvoiceId] = useState<number | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const selectedInvoice = invoices.data?.find((invoice) => invoice.id === selectedInvoiceId) ?? null;

  async function handleUpload(file: File) {
    setUploadError(null);
    try {
      await uploadInvoice(businessId, file);
      invoices.refresh();
    } catch (reason) {
      setUploadError(describeError(reason));
    }
  }

  async function handleDecision(invoiceId: number, decision: InvoiceDecision) {
    await decideInvoice(businessId, invoiceId, decision);
    invoices.refresh();
  }

  return (
    <div className={selectedInvoice ? "invoices-layout with-panel" : "invoices-layout"}>
      <div>
        <div className="toolbar">
          <UploadButton onUpload={handleUpload} />
        </div>
        {uploadError && <ErrorMessage message={uploadError} />}
        {invoices.error && <ErrorMessage message={invoices.error} />}
        {invoices.data ? (
          <InvoicesTable
            invoices={invoices.data}
            selectedInvoiceId={selectedInvoiceId}
            onSelectInvoice={setSelectedInvoiceId}
          />
        ) : (
          invoices.loading && <p className="muted">Loading invoices</p>
        )}
      </div>
      {selectedInvoice && (
        <InvoicePanel
          key={selectedInvoice.id}
          invoice={selectedInvoice}
          onDecide={(decision) => handleDecision(selectedInvoice.id, decision)}
          onClose={() => setSelectedInvoiceId(null)}
        />
      )}
    </div>
  );
}
