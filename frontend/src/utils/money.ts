const plainAmountFormatter = new Intl.NumberFormat("en-US", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

export function formatMoney(amount: string, currency: string): string {
  if (!currency) {
    return plainAmountFormatter.format(Number(amount));
  }
  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(Number(amount));
}
