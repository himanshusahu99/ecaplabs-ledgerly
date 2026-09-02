import { ApiError } from "../api/client";

const GENERIC_ERROR_MESSAGE = "Something went wrong. Please try again.";

export function describeError(reason: unknown): string {
  if (reason instanceof ApiError) {
    return reason.detail;
  }
  if (reason instanceof Error && reason.message) {
    return reason.message;
  }
  return GENERIC_ERROR_MESSAGE;
}
