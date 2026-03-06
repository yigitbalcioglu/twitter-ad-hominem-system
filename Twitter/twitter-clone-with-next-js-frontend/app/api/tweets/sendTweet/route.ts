import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";
import { refreshAccessToken } from "@/lib/refreshToken";
import { getApiBaseUrl } from "@/lib/api";

export async function POST(req: NextRequest) {
    try {
        const apiBaseUrl = getApiBaseUrl();
        const rawBody = await req.text();
        let parsedBody: { tweet?: string; parent?: string | null };

        try {
            parsedBody = JSON.parse(rawBody || "{}");
        } catch (parseError) {
            return NextResponse.json({ message: "Geçersiz JSON gövdesi." }, { status: 400 });
        }

        const tweet = (parsedBody.tweet ?? "").trim();
        const parent = parsedBody.parent ?? null;

        if (!tweet) {
            return NextResponse.json({ message: "Tweet boş olamaz." }, { status: 400 });
        }

        let accessToken: string | undefined = cookies().get("accessToken")?.value;

        let post = await fetch(`${apiBaseUrl}/tweets/`, {
            method: "POST",
            body: JSON.stringify({
                content: tweet,
                reply_to: parent ?? null,
            }),
            headers: {
                "Content-Type": "application/json",
                Authorization: accessToken ? `Bearer ${accessToken}` : "",
            },
        });

        if (post.status === 401) {
            const refreshed = await refreshAccessToken();
            accessToken = refreshed ?? undefined;
            if (accessToken) {
                post = await fetch(`${apiBaseUrl}/tweets/`, {
                    method: "POST",
                    body: JSON.stringify({
                        content: tweet,
                        reply_to: parent ?? null,
                    }),
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${accessToken}`,
                    },
                });
            }
        }

        if (!post.ok) {
            const errorMessage = await post.text();
            console.error("Django Error:", errorMessage);
            return NextResponse.json(
                { message: errorMessage || "Post failed." },
                { status: post.status },
            );
        }

        return NextResponse.json({ message: "Success" }, { status: 201 });
    } catch (error) {
        console.error("sendTweet route internal error:", error);
        return NextResponse.json({ message: "Internal Error" }, { status: 500 });
    }
}
