export interface Business {
  business_id: string;
  name: string;
}

export interface Me {
  email: string;
  businesses: Business[];
}

export type PaymentStatus = "pending" | "processing" | "settled" | "failed" | "cancelled";

export interface Payment {
  id: number;
  processor_payment_id: string;
  payee_name: string;
  amount: string;
  currency: string;
  status: PaymentStatus;
  memo: string;
  scheduled_for: string | null;
  created_at: string;
  updated_at: string;
}

export interface PaymentSummary {
  outstanding: string;
  settled_this_month: string;
  currency: string;
}

export type InvoiceStatus =
  | "uploaded"
  | "extracting"
  | "needs_review"
  | "approved"
  | "rejected"
  | "failed";

export type InvoiceDecision = "approve" | "reject";

export interface InvoiceLineItem {
  description: string;
  amount: string;
}

export interface Invoice {
  id: number;
  source_filename: string;
  status: InvoiceStatus;
  vendor_name: string;
  invoice_number: string;
  currency: string;
  total_amount: string | null;
  due_date: string | null;
  payee_id: number | null;
  payee_name: string | null;
  line_items: InvoiceLineItem[];
  extraction_error: string;
  document_text: string;
  created_at: string;
}
