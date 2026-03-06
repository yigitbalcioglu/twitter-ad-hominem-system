import "server-only";
import { cookies } from "next/headers";

import { getApiBaseUrl } from "./api";

export async function fetchApi(path: string, init: RequestInit = {}) {
  const token = cookies().get("accessToken")?.value;
  const url = `${getApiBaseUrl()}${path}`;
  const headers = new Headers(init.headers);

  if (token) {
    headers.set("Authorization", `Bearer ${token}`);
  }
  if (!headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  return fetch(url, { ...init, headers, cache: "no-store" });
}
