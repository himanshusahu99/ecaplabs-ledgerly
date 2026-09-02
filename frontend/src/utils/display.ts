export const PLACEHOLDER = "-";

export function textOrPlaceholder(value: string | null): string {
  return value ? value : PLACEHOLDER;
}
