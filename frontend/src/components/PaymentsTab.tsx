import { useMemo, useState } from "react";
import { usePayments } from "../hooks/usePayments";
import { usePaymentSummary } from "../hooks/usePaymentSummary";
import { filterPayments, PAYMENT_FILTER_OPTIONS, type PaymentFilter } from "../utils/paymentFilters";
import { ErrorMessage } from "./ErrorMessage";
import { FilterChips } from "./FilterChips";
import { PaymentsTable } from "./PaymentsTable";
import { SummaryCards } from "./SummaryCards";

interface PaymentsTabProps {
  businessId: string;
}

export function PaymentsTab({ businessId }: PaymentsTabProps) {
  const payments = usePayments(businessId);
  const summary = usePaymentSummary(businessId);
  const [filter, setFilter] = useState<PaymentFilter>("all");

  const visiblePayments = useMemo(() => filterPayments(payments.data ?? [], filter), [payments.data, filter]);
  const isRefreshing = payments.loading || summary.loading;

  function refreshAll() {
    payments.refresh();
    summary.refresh();
  }

  return (
    <>
      {summary.error && <ErrorMessage message={summary.error} />}
      <SummaryCards summary={summary.data} loading={summary.loading} />
      <div className="toolbar">
        <FilterChips label="Filter payments" options={PAYMENT_FILTER_OPTIONS} selected={filter} onSelect={setFilter} />
        <button type="button" className="button" onClick={refreshAll} disabled={isRefreshing}>
          {isRefreshing ? "Refreshing" : "Refresh"}
        </button>
      </div>
      {payments.error && <ErrorMessage message={payments.error} />}
      {payments.data ? (
        <PaymentsTable payments={visiblePayments} />
      ) : (
        payments.loading && <p className="muted">Loading payments</p>
      )}
    </>
  );
}
