"use client"

import React, { FC, } from 'react'
import { useRouter } from 'next/navigation';
import QueryString from 'qs';
import { ProfilePhoto } from '@/components/Image/ProfilePhoto';
import TweetsButtons from '../Button/TweetsButtons';

interface PostsListProps {
    post: ITweetProps;
    currentUserId: string;
    user: IUserProps
    url: string
    whosLikedTweet: LikeProp[]
    commentLength: number
    retweets: LikeProp[] | null
}

export const TweetonRoute: FC<PostsListProps> = ({ post, currentUserId, user, url, whosLikedTweet, commentLength, retweets }) => {
    const router = useRouter()

    const month = new Date(post.created_at).getMonth()
    const year = new Date(post.created_at).getFullYear()
    const hour = new Date(post.created_at).getHours()
    const minute = new Date(post.created_at).getMinutes()

    //kullanıcı id'leri olan bir string arrayi
    const usersWhoLikedTweet = whosLikedTweet.map(e => e.user)

    const months = [
        "Ocak",  // 0
        "Şubat", // 1
        "Mart",  // 2
        "Nisan", // 3
        "Mayıs", // 4
        "Haziran", // 5
        "Temmuz", // 6
        "Ağustos", // 7
        "Eylül", // 8
        "Ekim", // 9
        "Kasım", // 10
        "Aralık" // 11
    ];


    return (
        <>
            <div className="ml-4 cursor-pointer pb-4 pr-4" >
                <div className='flex'>
                    <ProfilePhoto
                        ownerId={post.author}
                        photo={url} />

                    <div onClick={() => {
                        router.push(`/tweet?${QueryString.stringify({
                            tweetId: `${post.id}`
                        })}`)
                    }} className='w-full'>
                        <div className=''>

                            <p className='text-white font-semibold mt-5 pl-1'>{user?.display_name ?? user?.username ?? 'Bilinmeyen Kullanici'}</p>
                            <p className='text-gray-500 pl-1'>@{user?.username ?? 'unknown'}</p>
                        </div>
                    </div>

                </div>
                <p className='mt-3 ml-1 break-words text-white'>{post.content}</p>
                <p className='text-gray-400 text-sm mt-2 ml-1'>
                    {post.is_ad_hominem ? 'Ad Hominem tespit edildi' : 'Ad hominem yok'}
                </p>
                <div className='ml-1 mr-2 mt-3 flex flex-wrap items-center gap-x-2 border-b-2 border-neutral-800 pb-6 text-gray-400 sm:mr-5'>
                    <p className='mt-1'>{hour}:{minute.toString().padStart(2, "0")}</p>
                    <p className='mx-2 '>.</p>
                    <p className='mt-1'>{months[month]} {year}</p></div>

            </div>
            <TweetsButtons
                currentUserId={currentUserId}
                post={post}
                user={user}
                commentLength={commentLength}
                whosLikedTweet={usersWhoLikedTweet}
                retweetLenght={retweets?.length} />
        </>
    )
}