import { getApiBaseUrl } from "@/lib/api";

type PaginatedResponse<T> = {
    results: T[];
};

export async function getComments(tweetId: string): Promise<ITweetProps[]> {
    try {
        const response = await fetch(`${getApiBaseUrl()}/tweets/?reply_to=${tweetId}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            return [];
        }

        const data = (await response.json()) as PaginatedResponse<ITweetProps>;
        return data.results;
    } catch (error) {
        return [];
    }
}

export async function getHomePageComments(tweets: ITweetProps[]): Promise<ITweetProps[]> {
    try {
        const fetchPromises = tweets.map((tweet) => {
            return fetch(`${getApiBaseUrl()}/tweets/?reply_to=${tweet.id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }).then((response) => response.json());
        });

        const responses = await Promise.all(fetchPromises);
        const allComments = responses.flatMap((response: PaginatedResponse<ITweetProps>) => response.results || []);

        return allComments;
    } catch (error) {
        return [];
    }
}
