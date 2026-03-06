import { UserProfile } from "@/components/profile/userProfile"
import { verifySession } from "@/lib/dal"
import { redirect } from "next/navigation"


interface ProfileProp {
    searchParams: {
        cameFrom?: string | string[]
    }
}

export default async function Profile({ searchParams }: ProfileProp) {
    const session = await verifySession()
    const cameFrom = searchParams?.cameFrom
    const profileId = Array.isArray(cameFrom) ? cameFrom[0] : cameFrom
    const url = (profileId ?? session.userId ?? "").trim()

    if (!url) {
        redirect("/")
    }

    return (
        <>
            <UserProfile
                profileId={url} />
        </>
    )
}


