import { cookies } from "next/headers";

const API_BASE_URL = (
  process.env.API_BASE_URL_INTERNAL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000/api/v1"
).replace(/\/$/, "");

export async function POST(request: Request) {
  const { email, password } = await request.json();

  const response = await fetch(`${API_BASE_URL}/auth/token/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    return Response.json({ detail: data?.detail || "Login failed" }, { status: response.status });
  }

  const data = await response.json();

  const secureCookie = process.env.NODE_ENV === "production";

  cookies().set("accessToken", data.access, {
    httpOnly: true,
    secure: secureCookie,
    sameSite: "lax",
    path: "/",
  });
  cookies().set("refreshToken", data.refresh, {
    httpOnly: true,
    secure: secureCookie,
    sameSite: "lax",
    path: "/",
  });

  return Response.json({ ok: true }, { status: 200 });
}
