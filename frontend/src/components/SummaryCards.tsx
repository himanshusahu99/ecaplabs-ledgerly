import type { PaymentSummary } from "../types";
import { formatMoney } from "../utils/money";

const SUMMARY_CARDS: ReadonlyArray<{ label: string; selectAmount: (summary: PaymentSummary) => string }> = [
  { label: "Outstanding", selectAmount: (summary) => summary.outstanding },
  { label: "Settled this month", selectAmount: (summary) => summary.settled_this_month },
];

interface SummaryCardsProps {
  summary: PaymentSummary | null;
  loading: boolean;
}

export function SummaryCards({ summary, loading }: SummaryCardsProps) {
  const unavailableText = loading ? "Loading" : "Unavailable";

  return (
    <div className="summary-cards">
      {SUMMARY_CARDS.map((card) => (
        <section key={card.label} className="summary-card" aria-label={card.label}>
          <h3 className="summary-label">{card.label}</h3>
          <p className="summary-value">
            {summary ? formatMoney(card.selectAmount(summary), summary.currency) : unavailableText}
          </p>
        </section>
      ))}
    </div>
  );
}
