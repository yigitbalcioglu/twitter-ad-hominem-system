import { getApiBaseUrl } from "@/lib/api";

type PaginatedResponse<T> = {
    results: T[];
};

export default async function fetchRelatedUsers(tweets: ITweetProps[]): Promise<IUserProps[] | null> {
    try {
        const ownerIds = [...new Set(tweets.map((tweet) => tweet.author))];
        if (ownerIds.length === 0) {
            return [];
        }

        const query = ownerIds.join(",");
        const response = await fetch(
            `${getApiBaseUrl()}/auth/users/?id__in=${query}&page_size=${ownerIds.length}`,
            {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        const data = (await response.json()) as PaginatedResponse<IUserProps> | IUserProps[];

        if (Array.isArray(data)) {
            return data;
        }

        return data.results ?? [];
    } catch (error) {
        console.error("Error fetching users:", error);
        return null;
    }
}
