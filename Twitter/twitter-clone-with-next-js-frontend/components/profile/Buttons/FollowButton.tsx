"use client"

import React, { useEffect, useState } from 'react'

interface Prop {
    userId: string;
    followState?: boolean;
    onFollowChange?: (value: boolean) => void;
}

export const FollowButton = ({ userId, followState: controlledFollowState, onFollowChange }: Prop) => {
    const [internalFollowState, setInternalFollowState] = useState<boolean>(false)
    const [isLoading, setIsLoading] = useState<boolean>(false)

    const followState = controlledFollowState ?? internalFollowState

    useEffect(() => {
        if (typeof controlledFollowState === "boolean") {
            setInternalFollowState(controlledFollowState)
        }
    }, [controlledFollowState])

    useEffect(() => {
        if (typeof controlledFollowState === "boolean") {
            return
        }

        const fetchFollowStatus = async () => {
            try {
                const response = await fetch(`/api/follows/status?userId=${userId}`, {
                    method: "GET",
                })

                if (!response.ok) {
                    return
                }

                const data = await response.json()
                const nextState = Boolean(data.following)
                setInternalFollowState(nextState)
                onFollowChange?.(nextState)
            } catch (error) {
                return
            }
        }

        fetchFollowStatus()
    }, [userId, controlledFollowState, onFollowChange])


    return (
        <button
            disabled={isLoading}
            onClick={async () => {
                setIsLoading(true)
                try {
                    const response = await fetch(`/api/follows/${userId}/toggle`, {
                        method: "POST",
                    })

                    if (!response.ok) {
                        return
                    }

                    const data = await response.json()
                    const nextState = Boolean(data.following)
                    setInternalFollowState(nextState)
                    onFollowChange?.(nextState)
                } catch (error) {
                    return
                } finally {
                    setIsLoading(false)
                }
            }} className={`h-9 rounded-3xl bg-[#009CFF] px-4 text-sm disabled:opacity-70 sm:w-24 sm:px-0`}
            type="submit">{followState ? "Takipten Çık" : "Takip Et"}</button>
    )
}
