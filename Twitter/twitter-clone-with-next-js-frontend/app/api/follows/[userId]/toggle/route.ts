import { cookies } from "next/headers";
import { refreshAccessToken } from "@/lib/refreshToken";

const API_BASE_URL = process.env.API_BASE_URL_INTERNAL ?? process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://web:8000/api/v1";

interface RouteContext {
  params: {
    userId: string;
  };
}

export async function POST(_: Request, { params }: RouteContext) {
  const userId = params.userId;
  let accessToken: string | undefined = cookies().get("accessToken")?.value;

  let response = await fetch(`${API_BASE_URL}/auth/follows/${userId}/toggle/`, {
    method: "POST",
    headers: {
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
  });

  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    accessToken = refreshed ?? undefined;

    if (accessToken) {
      response = await fetch(`${API_BASE_URL}/auth/follows/${userId}/toggle/`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
    }
  }

  if (!response.ok) {
    const data = await response.text();
    return Response.json({ detail: data || "Toggle failed" }, { status: response.status });
  }

  const data = await response.json();
  return Response.json(data, { status: response.status });
}
