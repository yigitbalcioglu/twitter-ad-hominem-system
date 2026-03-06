import { cookies } from "next/headers";
import { refreshAccessToken } from "@/lib/refreshToken";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export async function POST(request: Request) {
  const { tweetId } = await request.json();
  let accessToken: string | undefined = cookies().get("accessToken")?.value;

  let response = await fetch(`${API_BASE_URL}/retweets/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
    body: JSON.stringify({ tweet: tweetId }),
  });

  if (response.status === 401) {
    const refreshed = await refreshAccessToken();
    accessToken = refreshed ?? undefined;
    if (accessToken) {
      response = await fetch(`${API_BASE_URL}/retweets/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ tweet: tweetId }),
      });
    }
  }

  if (!response.ok) {
    const data = await response.text();
    return Response.json({ detail: data || "Retweet failed" }, { status: response.status });
  }

  return Response.json({ ok: true }, { status: 201 });
}

export async function DELETE(request: Request) {
  const { tweetId, userId } = await request.json();
  let accessToken: string | undefined = cookies().get("accessToken")?.value;

  let listResponse = await fetch(`${API_BASE_URL}/retweets/?tweet=${tweetId}&user=${userId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
  });

  if (listResponse.status === 401) {
    const refreshed = await refreshAccessToken();
    accessToken = refreshed ?? undefined;
    if (accessToken) {
      listResponse = await fetch(`${API_BASE_URL}/retweets/?tweet=${tweetId}&user=${userId}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${accessToken}`,
        },
      });
    }
  }

  if (!listResponse.ok) {
    return Response.json({ detail: "Retweet lookup failed" }, { status: listResponse.status });
  }

  const listData = await listResponse.json();
  const retweetId = listData.results?.[0]?.id;

  if (!retweetId) {
    return Response.json({ detail: "Retweet not found" }, { status: 404 });
  }

  let deleteResponse = await fetch(`${API_BASE_URL}/retweets/${retweetId}/`, {
    method: "DELETE",
    headers: {
      Authorization: accessToken ? `Bearer ${accessToken}` : "",
    },
  });

  if (deleteResponse.status === 401) {
    const refreshed = await refreshAccessToken();
    accessToken = refreshed ?? undefined;
    if (accessToken) {
      deleteResponse = await fetch(`${API_BASE_URL}/retweets/${retweetId}/`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${accessToken}`,
        },
      });
    }
  }

  if (!deleteResponse.ok) {
    return Response.json({ detail: "Delete failed" }, { status: deleteResponse.status });
  }

  return Response.json({ ok: true }, { status: 200 });
}
