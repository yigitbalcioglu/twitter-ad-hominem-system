import { cookies } from "next/headers";

const API_BASE_URL = process.env.API_BASE_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://web:8000/api/v1";

export async function refreshAccessToken(): Promise<string | null> {
  const refreshToken = cookies().get("refreshToken")?.value;
  if (!refreshToken) {
    return null;
  }

  const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ refresh: refreshToken }),
  });

  if (!response.ok) {
    return null;
  }

  const data = await response.json();
  const secureCookie = process.env.NODE_ENV === "production";

  cookies().set("accessToken", data.access, {
    httpOnly: true,
    secure: secureCookie,
    sameSite: "lax",
    path: "/",
  });

  return data.access as string;
}
