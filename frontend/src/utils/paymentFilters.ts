import type { Payment, PaymentStatus } from "../types";

export type PaymentFilter = "all" | "outstanding" | "settled" | "unsuccessful";

export const PAYMENT_FILTER_OPTIONS: ReadonlyArray<{ value: PaymentFilter; label: string }> = [
  { value: "all", label: "All" },
  { value: "outstanding", label: "Outstanding" },
  { value: "settled", label: "Settled" },
  { value: "unsuccessful", label: "Failed / Cancelled" },
];

const STATUSES_BY_FILTER: Record<Exclude<PaymentFilter, "all">, PaymentStatus[]> = {
  outstanding: ["pending", "processing"],
  settled: ["settled"],
  unsuccessful: ["failed", "cancelled"],
};

export function filterPayments(payments: Payment[], filter: PaymentFilter): Payment[] {
  if (filter === "all") {
    return payments;
  }
  const statuses = STATUSES_BY_FILTER[filter];
  return payments.filter((payment) => statuses.includes(payment.status));
}
