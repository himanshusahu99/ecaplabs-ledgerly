import { useCallback } from "react";
import { fetchInvoices } from "../api/invoices";
import type { Invoice } from "../types";
import { useApiResource, type ApiResource } from "./useApiResource";

export function useInvoices(businessId: string): ApiResource<Invoice[]> {
  const load = useCallback(() => fetchInvoices(businessId), [businessId]);
  return useApiResource(load);
}
