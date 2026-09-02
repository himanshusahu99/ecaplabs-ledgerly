import { useCallback } from "react";
import { fetchPaymentSummary } from "../api/payments";
import type { PaymentSummary } from "../types";
import { useApiResource, type ApiResource } from "./useApiResource";

export function usePaymentSummary(businessId: string): ApiResource<PaymentSummary> {
  const load = useCallback(() => fetchPaymentSummary(businessId), [businessId]);
  return useApiResource(load);
}
