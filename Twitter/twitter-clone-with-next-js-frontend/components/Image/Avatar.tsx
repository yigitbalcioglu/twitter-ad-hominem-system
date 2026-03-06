"use client"

import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import getPhoto from '@/hooks/getPhoto'

interface ownersIdProp {
    ownersId: string;
}


export const Avatar = ({ ownersId }: ownersIdProp) => {
    const [url, setUrl] = useState<string>("");

    useEffect(() => {
        const fetchPhoto = async () => {
            try {
                const photoUrl = await getPhoto(ownersId);
                setUrl(photoUrl);
            } catch (error) {
                console.error("Error fetching photo:", error);
            }
        };

        fetchPhoto();
    }, [ownersId]);

    return (
        <Image alt="photo"
            src={url && url.startsWith("http") ? url : url || "https://placehold.co/48x48/png"}
            width={128}
            height={128}
            className="bg-cover transform w-12 h-12 bg-white rounded-full border-4 border-black overflow-hidden" />
    )
}
