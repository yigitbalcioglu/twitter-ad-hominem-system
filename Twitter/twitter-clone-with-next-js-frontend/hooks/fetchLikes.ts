import { getApiBaseUrl } from "@/lib/api";

type PaginatedResponse<T> = {
    results: T[];
};

export const fetchLikes = async (tweets: ITweetProps[]): Promise<LikeProp[]> => {
    const tweetIds = tweets?.map((tweet) => tweet.id) ?? [];

    try {
        const responses = await Promise.all(
            tweetIds.map((id) =>
                fetch(`${getApiBaseUrl()}/likes/?tweet=${id}&page_size=100`, {
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

        const likes = responses.flatMap((response: PaginatedResponse<LikeProp>) => response.results || []);
        return likes;
    } catch (error) {
        return [];
    }
};

export const getSingleTweetsLikes = async (tweets: ITweetProps): Promise<LikeProp[]> => {
    try {
        const response = await fetch(`${getApiBaseUrl()}/likes/?tweet=${tweets.id}&page_size=100`, {
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