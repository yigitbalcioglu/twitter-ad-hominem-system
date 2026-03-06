import { cookies } from "next/headers";
import { refreshAccessToken } from "@/lib/refreshToken";
import { getApiBaseUrl } from "@/lib/api";

export async function GET() {
  const apiBaseUrl = getApiBaseUrl();
  let accessToken: string | undefined = cookies().get("accessToken")?.value;

  let response = await fetch(`${apiBaseUrl}/auth/messages/contacts/`, {
    method: "GET",
    headers: {
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
  });

  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    accessToken = refreshed ?? undefined;

    if (accessToken) {
      response = await fetch(`${apiBaseUrl}/auth/messages/contacts/`, {
        method: "GET",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
    }
  }

  if (!response.ok) {
    const data = await response.text();
    return Response.json({ detail: data || "Could not fetch contacts" }, { status: response.status });
  }

  const data = await response.json();
  return Response.json(data, { status: 200 });
}
