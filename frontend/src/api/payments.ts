import type { Payment, PaymentSummary } from "../types";
import { apiRequest } from "./client";

function paymentsPath(businessId: string): string {
  return `/businesses/${encodeURIComponent(businessId)}/payments/`;
}

export function fetchPayments(businessId: string): Promise<Payment[]> {
  return apiRequest<Payment[]>(paymentsPath(businessId));
}

export function fetchPaymentSummary(businessId: string): Promise<PaymentSummary> {
  return apiRequest<PaymentSummary>(`${paymentsPath(businessId)}summary/`);
}
