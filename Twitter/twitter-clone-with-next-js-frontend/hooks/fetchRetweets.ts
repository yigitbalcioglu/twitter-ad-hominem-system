import { getApiBaseUrl } from "@/lib/api";

type PaginatedResponse<T> = {
    results: T[];
};

export const fetchRetweets = async (tweets: ITweetProps[]): Promise<LikeProp[]> => {
    const tweetIds = tweets?.map((tweet) => tweet.id) ?? [];

    try {
        const responses = await Promise.all(
            tweetIds.map((id) =>
                fetch(`${getApiBaseUrl()}/retweets/?tweet=${id}&page_size=100`, {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                    },
                }).then(async (response) => {
                    if (!response.ok) {
                        return { results: [] } as PaginatedResponse<LikeProp>;
                    }
                    return (await response.json()) as PaginatedResponse<LikeProp>;
                })
            )
        );

        const retweets = responses.flatMap((response: PaginatedResponse<LikeProp>) => response.results || []);
        return retweets;
    } catch (error) {
        return [];
    }
};

export const getSingleTweetsRetweets = async (tweets: ITweetProps): Promise<LikeProp[]> => {
    try {
        const response = await fetch(`${getApiBaseUrl()}/retweets/?tweet=${tweets.id}&page_size=100`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            return [];
        }

        const data = (await response.json()) as PaginatedResponse<LikeProp>;
        return data.results;
    } catch (error) {
        return [];
    }
};