"use client"

import React, { useEffect, useState } from 'react'
import { EditButton } from './Buttons/EditButton';
import { SendMessageButton } from './Buttons/SendMessageButton';
import { FollowButton } from './Buttons/FollowButton';

interface Prop {
    userId: string;
    currentUserId: string;
}

export default function UserBioButtons({ userId, currentUserId }: Prop) {
    const [isFollowing, setIsFollowing] = useState<boolean>(false)

    useEffect(() => {
        if (!currentUserId || currentUserId === userId) {
            return
        }

        const fetchFollowStatus = async () => {
            try {
                const response = await fetch(`/api/follows/status?userId=${userId}`, {
                    method: "GET",
                })

                if (!response.ok) {
                    setIsFollowing(false)
                    return
                }

                const data = await response.json()
                setIsFollowing(Boolean(data.following))
            } catch (error) {
                setIsFollowing(false)
            }
        }

        fetchFollowStatus()
    }, [currentUserId, userId])


    return (
        <div className='text-white'>
            {currentUserId === userId ?
                (<EditButton />)
                :
                (<div className='flex flex-wrap gap-2'>
                    {isFollowing && <SendMessageButton userId={userId} />}
                    <FollowButton
                        userId={userId}
                        followState={isFollowing}
                        onFollowChange={setIsFollowing}
                    />
                </div>)}
        </div>
    )
}
