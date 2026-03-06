export const handleRetweet = async (userId: string, tweetId: string) => {
    try {
        const response = await fetch(`/api/retweets`, {
            method: "POST",
            body: JSON.stringify({
                userId,
                tweetId,
            }),
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error("Post failed.");
        }

        return Response.json({ message: "Success" }, { status: 201 });
    } catch (error) {
        throw error;
    }
};
export const handleRemoveRetweet = async (userId: string, tweetId: string) => {
    try {
        const response = await fetch(`/api/retweets`, {
            method: "DELETE",
            body: JSON.stringify({
                userId,
                tweetId,
            }),
            headers: {
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error("Delete failed.");
        }

        return { message: "Success" };
    } catch (error) {
        console.error("Error:", error);
        throw error;
    }
};





