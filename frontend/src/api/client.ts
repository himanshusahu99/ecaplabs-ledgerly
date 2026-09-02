export class ApiError extends Error {
  readonly status: number;
  readonly detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.name = "ApiError";
    this.status = status;
    this.detail = detail;
  }
}

const API_BASE_PATH = "/api";

function hasDetail(body: unknown): body is { detail: string } {
  return typeof body === "object" && body !== null && typeof (body as { detail?: unknown }).detail === "string";
}

async function readErrorDetail(response: Response): Promise<string> {
  const fallback = response.statusText || `Request failed with status ${response.status}`;
  const body: unknown = await response.json().catch(() => null);
  return hasDetail(body) ? body.detail : fallback;
}

export async function apiRequest<T>(path: string, init: RequestInit = {}): Promise<T> {
  const headers = new Headers(init.headers);
  headers.set("Authorization", `Token ${import.meta.env.VITE_API_TOKEN}`);
  headers.set("Accept", "application/json");

  const response = await fetch(`${API_BASE_PATH}${path}`, { ...init, headers });
  if (!response.ok) {
    throw new ApiError(response.status, await readErrorDetail(response));
  }
  return (await response.json()) as T;
}
