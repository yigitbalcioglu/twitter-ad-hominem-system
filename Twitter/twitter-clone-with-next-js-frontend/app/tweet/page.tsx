import React from 'react'
import { verifySession } from '@/lib/dal';
import getOneTweet from '@/hooks/getOneTweet';
import { RelatedComments } from '@/components/Comment/RelatedComments';
import { getComments, getHomePageComments } from '@/hooks/getComments';
import GetUser from '@/hooks/getUser';
import { TweetonRoute } from '@/components/Tweets/Tweet Component/TweetonRoute';
import SendPost from '@/components/Tweets/Send Tweet/SendPost';
import getPhoto from '@/hooks/getPhoto';
import { fetchLikes, getSingleTweetsLikes } from '@/hooks/fetchLikes';
import fetchRelatedUsers from '@/hooks/fetchTweetsUsers';
import { fetchRetweets, getSingleTweetsRetweets } from '@/hooks/fetchRetweets';

interface searchParamsProp {
    searchParams: {
        tweetId: string;
    }
}

export default async function page({ searchParams }: searchParamsProp) {
    const session = await verifySession()
    const post = await getOneTweet({ searchParams })
    const id = session.userId

    if (!post) {
        return <div className="text-white">Tweet bulunamadi.</div>
    }

    const owner = await GetUser(post.author)
    if (!owner) {
        return <div className="text-white">Kullanici bulunamadi.</div>
    }

    // ana tweetin mentleri
    const comments = await getComments(post.id)

    //alttaki mentlerin mentleri
    const commentsOfComments = await getHomePageComments(comments)

    const users = (await fetchRelatedUsers(comments)) ?? []
    const likes = await getSingleTweetsLikes(post)
    const commentsLikes = await fetchLikes(comments)

    //retweets
    const postsRetweets = await getSingleTweetsRetweets(post)
    const retweets = await fetchRetweets(comments)


    return (
        <div>
            <TweetonRoute
                currentUserId={session.userId}
                post={post}
                user={owner}
                whosLikedTweet={likes}
                commentLength={comments?.length}
                url={await getPhoto(owner.id)}
                retweets={postsRetweets}
            />

            <SendPost
                mode="Cevap"
                userId={id}
                photoUrl={await getPhoto(id)}
                post={post}
            />

            <RelatedComments
                currentUserId={session.userId}
                users={users}
                post={post}
                comments={comments}
                whosLikedTweet={commentsLikes}
                secondaryComments={commentsOfComments}
                retweets={retweets}
            />
        </div>
    )
}
