import { fetchMe } from "../api/me";
import type { Me } from "../types";
import { useApiResource, type ApiResource } from "./useApiResource";

export function useMe(): ApiResource<Me> {
  return useApiResource(fetchMe);
}
