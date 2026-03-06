"use client"

import React from 'react'
import { Tweet } from '../Tweet Component/Tweet';

interface PostsListProps {
    userId: string
    tweets: ITweetProps[]
    users: IUserProps[]
    urls: IUserPhotoProps[]
    likes: LikeProp[]
    comments: ITweetProps[]
}

const HomePageTweets = ({ userId, tweets, users, urls, likes, comments }: PostsListProps) => {

    return (
        <div>
            {tweets && tweets.length > 0 ?
                (
                    <ul>
                        {tweets.map((tweet) => {
                            const tweetOwner = users.find(u => u.id === tweet.author);
                            if (!tweetOwner) {
                                return null;
                            }
                            const url = urls.find(u => u.userId === tweet.author)
                            const usersWhoLikedTweet = likes.filter(like => like.tweet === tweet.id).map(e => e.user)
                            const relatedComments = comments.filter(comment => comment.reply_to === tweet.id)

                            return (
                                <li key={tweet.id}>
                                    <div className='pb-4'>
                                        <Tweet
                                            currentUserId={userId}
                                            post={tweet}
                                            user={tweetOwner}
                                            url={url?.photoUrl!}
                                            whosLikedTweet={usersWhoLikedTweet}
                                            comments={relatedComments}
                                        />
                                    </div>
                                </li>
                            )
                        })}
                    </ul>
                ) : (
                    <p>{null}</p>
                )
            }
        </div >
    );
};

export default HomePageTweets;
