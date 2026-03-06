"use client"

import React from 'react'
import { useRouter } from 'next/navigation'
import QueryString from 'qs'

interface IPostProp {
    post: ITweetProps
    user: IUserProps
}

const Post = ({ post, user }: IPostProp) => {

    const month = new Date(post.created_at).getMonth()
    const year = new Date(post.created_at).getFullYear()
    const hour = new Date(post.created_at).getHours()
    const minute = new Date(post.created_at).getMinutes()

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


    const router = useRouter()

    return (
        <div onClick={() => {
            router.push(`/tweet?${QueryString.stringify({
                tweetId: `${post.id}`
            })}`)
        }}
            className='w-full pr-2'>
            <div className='mt-5 flex flex-wrap items-center gap-x-1 gap-y-1 text-sm sm:text-base'>
                <p className='font-semibold text-white'>{user?.display_name ?? user?.username ?? 'Bilinmeyen Kullanici'}</p>
                <p className='text-gray-500'>@{user?.username ?? 'unknown'}</p>
                <p className='text-gray-500'>·</p>
                <p className='text-gray-500'>{hour}:{minute.toString().padStart(2, "0")}</p>
                <p className='ml-1 text-gray-500'>{months[month]} {year}</p>
            </div>
            <p className='break-words text-white'>{post.content}</p>
            <p className='text-gray-400 text-sm mt-2'>
                {post.is_ad_hominem ? 'Ad Hominem tespit edildi' : 'Ad hominem yok'}
            </p>
        </div>
    )
}

export default Post