"use client"
import React, { useEffect, useState } from 'react'
import { FaLocationDot } from "react-icons/fa6";
import { FaCalendarAlt } from "react-icons/fa";
import GetUser from '@/hooks/getUser';

interface UserBioProp {
    userId: string
}

export const UserBio: React.FC<UserBioProp> = ({ userId }) => {

    const [userData, setUserData] = useState<IUserProps | null>(null);

    useEffect(() => {
        const fetchCurrentUser = async () => {
            try {
                const user = await GetUser(userId);
                setUserData(user);
            } catch (error) {
                setUserData(null);
            }
        };

        fetchCurrentUser();
    }, [userId]);


    return (
        <div className='pb-4'>
            <div className='mt-14 text-white sm:ml-4 sm:mt-20'>
                <h1 className='text-lg font-extrabold sm:text-xl'>{userData?.display_name ?? userData?.username}</h1>
                <h3 className='font-medium text-gray-500'>@{userData?.username}</h3>
            </div>
            <div className='mt-4 flex flex-wrap items-center gap-2 text-sm text-gray-500 sm:ml-5 sm:text-base'>
                <FaLocationDot />
                <p>{userData?.location}</p>
                <div className='flex items-center gap-1 sm:ml-4'>
                    <FaCalendarAlt />
                    <p>{userData?.date_joined} tarihinde katildi</p>
                </div>
            </div>
            <div className='mt-4 flex flex-wrap items-center gap-x-3 gap-y-1 sm:ml-5'>
                <p className='text-white mr-1'>{userData?.following_count ?? 0}</p>
                <p className='text-gray-500 mr-4'> Takip edilen</p>
                <p className='text-white mr-1'>{userData?.followers_count ?? 0}</p>
                <p className='text-gray-500'> Takipçi</p>
            </div>
            <div className='mt-4 flex flex-wrap text-sm text-gray-500 sm:ml-5'>
                <p className='pr-1'>Random User</p>
                <p className='pr-1'>ve takip ettiğin diğer</p>
                <p className='pr-1'>Ortak takipçi sayısı</p>
                <p>kişi tarafından takip ediliyor.</p>
            </div>
        </div>
    )
}
