import React from 'react'
import { verifySession } from '@/lib/dal'
import { UserHeader } from './userHeader'
import { UserPhoto } from './userPhoto'
import { UserBio } from './userBio'
import { UserButtons } from './userButtons'
import UserBioButtons from './userBioButtons'

interface UserProfileProp {
    profileId: string
}

export const UserProfile = async ({ profileId }: UserProfileProp) => {
    const session = await verifySession()
    const viewerId = session.userId

    return (
        <div>
            <UserHeader />
            <UserPhoto userId={profileId} />
            <div className='flex flex-col gap-4 px-4 pt-4 sm:flex-row sm:items-start sm:justify-between sm:px-0 sm:pt-0'>
                <UserBio userId={profileId} />
                <div className='sm:m-5'>
                    <UserBioButtons userId={profileId} currentUserId={viewerId} />
                </div>
            </div>
            <UserButtons profileId={profileId} currentUserId={viewerId} />
        </div>
    )
}
