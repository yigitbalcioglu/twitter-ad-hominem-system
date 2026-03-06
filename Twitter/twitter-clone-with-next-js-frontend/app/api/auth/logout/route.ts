import { cookies } from "next/headers";

export async function POST() {
  cookies().delete("accessToken");
  cookies().delete("refreshToken");
  return Response.json({ ok: true }, { status: 200 });
}
