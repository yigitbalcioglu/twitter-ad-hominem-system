const DEFAULT_API_BASE_URL = "http://localhost:8000/api/v1";
const DEFAULT_INTERNAL_API_BASE_URL = "http://web:8000/api/v1";

export function getApiBaseUrl(): string {
  if (typeof window === "undefined") {
    return process.env.API_BASE_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_INTERNAL_API_BASE_URL;
  }

  return process.env.NEXT_PUBLIC_API_BASE_URL ?? DEFAULT_API_BASE_URL;
}

export async function fetchPublic(path: string, init: RequestInit = {}) {
  const url = `${getApiBaseUrl()}${path}`;
  const headers = new Headers(init.headers);

  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  return fetch(url, { ...init, headers, cache: "no-store" });
}
