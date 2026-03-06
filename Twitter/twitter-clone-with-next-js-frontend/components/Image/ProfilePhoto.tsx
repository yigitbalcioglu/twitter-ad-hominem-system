"use client"

import Image from 'next/image'
import QueryString from 'qs'
import React from 'react'
import { useRouter } from 'next/navigation'

interface IProfilePhotoProps {
  ownerId: string
  photo: string
}

export const ProfilePhoto: React.FC<IProfilePhotoProps> = ({ ownerId, photo }) => {

  const router = useRouter()

  return (
    <>
      <Image onClick={() => {
        router.push(`/profile?${QueryString.stringify({ cameFrom: `${ownerId}` })}`)
      }}
        src={photo && photo.startsWith("http") ? photo : photo || "https://placehold.co/48x48/png"}
        alt='photo'
        width={30}
        height={30}
        className="bg-cover ml-2 mt-4 transform w-12 h-12 bg-white rounded-full border-4 border-black overflow-hidden" />
    </>
  )
}
