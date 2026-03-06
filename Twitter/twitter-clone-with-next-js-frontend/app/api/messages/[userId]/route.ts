import { cookies } from "next/headers";
import { refreshAccessToken } from "@/lib/refreshToken";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

interface RouteContext {
  params: {
    userId: string;
  };
}

export async function GET(_: Request, { params }: RouteContext) {
  const userId = params.userId;
  let accessToken: string | undefined = cookies().get("accessToken")?.value;

  let response = await fetch(`${API_BASE_URL}/auth/messages/${userId}/`, {
    method: "GET",
    headers: {
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
  });

  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    accessToken = refreshed ?? undefined;

    if (accessToken) {
      response = await fetch(`${API_BASE_URL}/auth/messages/${userId}/`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
    }
  }

  if (!response.ok) {
    const data = await response.text();
    return Response.json({ detail: data || "Could not fetch messages" }, { status: response.status });
  }

  const data = await response.json();
  return Response.json(data, { status: 200 });
}

export async function POST(request: Request, { params }: RouteContext) {
  const userId = params.userId;
  const { text } = await request.json();
  let accessToken: string | undefined = cookies().get("accessToken")?.value;

  let response = await fetch(`${API_BASE_URL}/auth/messages/${userId}/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
    body: JSON.stringify({ text }),
  });

  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    accessToken = refreshed ?? undefined;

    if (accessToken) {
      response = await fetch(`${API_BASE_URL}/auth/messages/${userId}/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ text }),
      });
    }
  }

  if (!response.ok) {
    const data = await response.text();
    return Response.json({ detail: data || "Could not send message" }, { status: response.status });
  }

  const data = await response.json();
  return Response.json(data, { status: response.status });
}
