import { cookies } from "next/headers";
import { refreshAccessToken } from "@/lib/refreshToken";

const API_BASE_URL = process.env.API_BASE_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://web:8000/api/v1";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const userId = searchParams.get("userId");

  const endpoint = userId
    ? `${API_BASE_URL}/auth/follows/following/?user_id=${userId}`
    : `${API_BASE_URL}/auth/follows/following/`;

  let accessToken: string | undefined = cookies().get("accessToken")?.value;

  let response = await fetch(endpoint, {
    method: "GET",
    headers: {
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
  });

  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    accessToken = refreshed ?? undefined;

    if (accessToken) {
      response = await fetch(endpoint, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
    }
  }

  if (!response.ok) {
    const data = await response.text();
    return Response.json({ detail: data || "Could not fetch following list" }, { status: response.status });
  }

  const data = await response.json();
  return Response.json(data, { status: 200 });
}
