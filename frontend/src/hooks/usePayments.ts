import { useCallback } from "react";
import { fetchPayments } from "../api/payments";
import type { Payment } from "../types";
import { useApiResource, type ApiResource } from "./useApiResource";

export function usePayments(businessId: string): ApiResource<Payment[]> {
  const load = useCallback(() => fetchPayments(businessId), [businessId]);
  return useApiResource(load);
}
