export const postRequest = async (tweetBody: string, parent: string | null) => {
    const response = await fetch("/api/tweets/sendTweet", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            tweet: tweetBody,
            parent: parent,
        }),
    });

    if (!response.ok) {
        throw new Error("Tweet gonderimi basarisiz oldu.");
    }
};