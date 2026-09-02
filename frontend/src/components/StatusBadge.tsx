import type { InvoiceStatus, PaymentStatus } from "../types";

type BadgeTone = "neutral" | "info" | "warning" | "success" | "danger" | "muted";

const TONE_BY_STATUS: Record<PaymentStatus | InvoiceStatus, BadgeTone> = {
  pending: "neutral",
  processing: "info",
  settled: "success",
  failed: "danger",
  cancelled: "muted",
  uploaded: "neutral",
  extracting: "info",
  needs_review: "warning",
  approved: "success",
  rejected: "muted",
};

interface StatusBadgeProps {
  status: PaymentStatus | InvoiceStatus;
}

export function StatusBadge({ status }: StatusBadgeProps) {
  return <span className={`status-badge tone-${TONE_BY_STATUS[status]}`}>{status.replace("_", " ")}</span>;
}
