import "server-only";

import { redirect } from "next/navigation";
import { cache } from "react";
import { fetchApi } from "./serverApi";

export const verifySession = cache(async () => {
    const response = await fetchApi("/auth/me/");

    if (!response.ok) {
        redirect("/login");
        return { isAuth: false, userId: "" };
    }

    const user = await response.json();
    return { isAuth: true, userId: user.id as string };
});

export const getUser = cache(async () => {
    const session = await verifySession();

    if (!session?.isAuth) return null;

    try {
        const response = await fetchApi("/auth/me/");
        if (!response.ok) {
            throw new Error("Kullanici bulunamadi.");
        }
        return await response.json();
    } catch (error) {
        console.log("Failed to fetch user");
        return null;
    }
});