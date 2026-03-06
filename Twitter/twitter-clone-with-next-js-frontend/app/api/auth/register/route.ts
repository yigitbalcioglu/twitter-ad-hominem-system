const API_BASE_URL = (
  process.env.API_BASE_URL_INTERNAL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000/api/v1"
).replace(/\/$/, "");

export async function POST(request: Request) {
  const { email, username, password } = await request.json();

  const response = await fetch(`${API_BASE_URL}/auth/register/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, username, password }),
  });

  if (!response.ok) {
    const data = await response.json().catch(() => null);
    return Response.json(data ?? { detail: "Register failed" }, { status: response.status });
  }

  return Response.json({ ok: true }, { status: 201 });
}
