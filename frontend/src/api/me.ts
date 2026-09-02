import type { Me } from "../types";
import { apiRequest } from "./client";

export function fetchMe(): Promise<Me> {
  return apiRequest<Me>("/me/");
}
