import type { Invoice, InvoiceDecision } from "../types";
import { apiRequest } from "./client";

function invoicesPath(businessId: string): string {
  return `/businesses/${encodeURIComponent(businessId)}/invoices/`;
}

export function fetchInvoices(businessId: string): Promise<Invoice[]> {
  return apiRequest<Invoice[]>(invoicesPath(businessId));
}

export function uploadInvoice(businessId: string, file: File): Promise<Invoice> {
  const formData = new FormData();
  formData.append("file", file);
  return apiRequest<Invoice>(invoicesPath(businessId), { method: "POST", body: formData });
}

export function decideInvoice(
  businessId: string,
  invoiceId: number,
  decision: InvoiceDecision,
): Promise<Invoice> {
  return apiRequest<Invoice>(`${invoicesPath(businessId)}${invoiceId}/${decision}/`, { method: "POST" });
}
