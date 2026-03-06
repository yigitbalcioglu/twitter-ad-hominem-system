"use client"
import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import GetUser from '@/hooks/getUser';


interface UserPhotoProps {
    userId: string; // Define the type of profileId as string
}

export const UserPhoto: React.FC<UserPhotoProps> = ({ userId }) => {
    const [photo, setPhoto] = useState<string>()
    const [header, setHeader] = useState<string>()

    useEffect(() => {
        const fetchPhotos = async () => {
            try {
                const user = await GetUser(userId)
                setPhoto(user?.avatar)
                setHeader(user?.banner)

            } catch (error) {
                setPhoto(undefined)
                setHeader(undefined)
            }
        }

        fetchPhotos();
    }, [userId]);

    return (
        <div className="text-white w-full h-full">
            <div className="relative w-full h-40 bg-slate-50">
                {header && (
                    <div
                        className="absolute inset-0 w-full h-full bg-cover bg-center"
                        style={{ backgroundImage: `url('${header}')` }}
                    />
                )}
                <div className="absolute -bottom-14 left-4 h-[6.5rem] w-[6.5rem] overflow-hidden rounded-full border-4 border-black bg-white sm:-bottom-[60px] sm:left-8 sm:h-[7.5rem] sm:w-[7.5rem]">
                    {photo && (
                        <Image
                            alt="photo"
                            src={photo}
                            width={128}
                            height={128}
                            className="object-fill w-full h-full"
                        />
                    )}
                </div>
            </div>

        </div>

    )
}
