"use client"

import { useState, useEffect } from "react";
import { Tweet } from "../Tweets/Tweet Component/Tweet";
import GetUser from "@/hooks/getUser";
import { getApiBaseUrl } from "@/lib/api";

interface PostsListProps {
    userId: string;
    currentUserId: string;
}

type PaginatedResponse<T> = {
    results: T[];
};

export const UserTweets = ({ userId, currentUserId }: PostsListProps) => {

    const [posts, setPosts] = useState<ITweetProps[]>([]);
    const [user, setUser] = useState<IUserProps | null>(null);

    useEffect(() => {
        const fetchTweets = async () => {
            try {

                const response = await fetch(
                    `${getApiBaseUrl()}/tweets/?author=${userId}&reply_to__isnull=true`,
                    {
                        method: 'GET',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }
                );

                if (!response.ok) {
                    setPosts([]);
                    return;
                }

                const data = (await response.json()) as PaginatedResponse<ITweetProps>;
                setPosts(data.results);

                const fetchedUser = await GetUser(userId);
                setUser(fetchedUser);
            } catch (error) {
                setPosts([]);
                setUser(null);
            }
        };

        fetchTweets();
    }, [userId]);
    return (
        <div>
            <ul>
                {posts.map((post) => (
                    <li key={post.id}>
                        {user && (
                            <Tweet
                                user={user}
                                currentUserId={currentUserId}
                                post={post} />
                        )}

                    </li>
                ))}
            </ul>
        </div >
    )
}
