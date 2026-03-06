"use client"

import React from 'react'
import { useRouter } from 'next/navigation'

interface Prop {
    userId: string;
}

export const SendMessageButton = ({ userId }: Prop) => {

    const router = useRouter()
    return (
        <button className={`h-9 rounded-3xl bg-[#009CFF] px-4 text-sm sm:w-24 sm:px-0`}
            type="submit" onClick={() => {
                router.push(`/messages?to=${userId}`)
            }}>Mesaj At</button>
    )
}
