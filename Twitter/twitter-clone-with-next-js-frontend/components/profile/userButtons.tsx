"use client"

import React, { useState } from 'react'
import { UserFollowers } from './userFollowers'
import { UserFollowings } from './userFollowings'
import { UserTweets } from './userTweets'

interface UserButtonsProps {
    profileId: string
    currentUserId: string
}

type ProfileTab = "tweets" | "following" | "followers"

export const UserButtons = ({ profileId, currentUserId }: UserButtonsProps) => {
    const [activeTab, setActiveTab] = useState<ProfileTab>("tweets")

    return (
        <div>
            <div className='mt-6 grid grid-cols-3 border-b-[0.1px] border-gray-600 pb-3 text-sm font-semibold text-white sm:text-base'>
                <button
                    onClick={() => setActiveTab("tweets")}
                    className={`px-2 py-2 ${activeTab === "tweets" ? "text-sky-400" : "text-white"}`}
                >
                    Gönderiler
                </button>
                <button
                    onClick={() => setActiveTab("following")}
                    className={`px-2 py-2 ${activeTab === "following" ? "text-sky-400" : "text-white"}`}
                >
                    Takip Ettiklerim
                </button>
                <button
                    onClick={() => setActiveTab("followers")}
                    className={`px-2 py-2 ${activeTab === "followers" ? "text-sky-400" : "text-white"}`}
                >
                    Takipçilerim
                </button>
            </div>

            {activeTab === "tweets" && <UserTweets userId={profileId} currentUserId={currentUserId} />}
            {activeTab === "following" && <UserFollowings userId={profileId} />}
            {activeTab === "followers" && <UserFollowers userId={profileId} />}
        </div>
    )
}
