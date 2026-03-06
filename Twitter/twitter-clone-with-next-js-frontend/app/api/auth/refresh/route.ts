import { refreshAccessToken } from "@/lib/refreshToken";

export async function POST() {
  const token = await refreshAccessToken();
  if (!token) {
    return Response.json({ detail: "Refresh failed" }, { status: 401 });
  }
  return Response.json({ ok: true }, { status: 200 });
}
