import { getApiBaseUrl } from "@/lib/api";

type PaginatedResponse<T> = {
    results: T[];
};

export async function FetchTweets(amount: number): Promise<ITweetProps[]> {
    try {
        const response = await fetch(
            `${getApiBaseUrl()}/tweets/?reply_to__isnull=true&page_size=${amount}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }
        );

        if (!response.ok) {
            return [];
        }

        const data = (await response.json()) as PaginatedResponse<ITweetProps>;
        return data.results;
    } catch (error) {
        return [];
    }
}
