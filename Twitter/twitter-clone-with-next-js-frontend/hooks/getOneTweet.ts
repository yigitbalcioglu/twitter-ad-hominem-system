import { getApiBaseUrl } from "@/lib/api";

interface searchParamsProp {
    searchParams: {
        tweetId: string;
    };
}

const getOneTweet = async ({ searchParams }: searchParamsProp): Promise<ITweetProps | null> => {
    try {
        const response = await fetch(`${getApiBaseUrl()}/tweets/${searchParams.tweetId}/`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            return null;
        }

        const data = (await response.json()) as ITweetProps;
        return data;
    } catch (error) {
        return null;
    }
};

export default getOneTweet;