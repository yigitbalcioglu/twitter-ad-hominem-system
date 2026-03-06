import { getApiBaseUrl } from "@/lib/api";

export const fetchUsername = async (tweetId: string) => {
    try {
        const response = await fetch(`${getApiBaseUrl()}/auth/users/${tweetId}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            return "Unknown User";
        }

        const user = (await response.json()) as IUserProps;
        return user ? user.username : "Unknown User";
    } catch (error) {
        console.error("Unexpected error occurred while fetching username:", error);
        return "Unknown User";
    }
};