"use client"

import Link from "next/link"
import { useEffect, useState } from "react"

interface UserFollowersProps {
	userId: string
}

type UserListResponse = {
	results?: IUserProps[]
}

export const UserFollowers = ({ userId }: UserFollowersProps) => {
	const [users, setUsers] = useState<IUserProps[]>([])
	const [loading, setLoading] = useState<boolean>(true)

	useEffect(() => {
		const fetchFollowers = async () => {
			setLoading(true)
			try {
				const response = await fetch(`/api/follows/followers?userId=${userId}`, { method: "GET" })
				if (!response.ok) {
					setUsers([])
					return
				}

				const data = (await response.json()) as IUserProps[] | UserListResponse
				const parsedUsers = Array.isArray(data) ? data : (data.results ?? [])
				setUsers(parsedUsers)
			} catch (error) {
				setUsers([])
			} finally {
				setLoading(false)
			}
		}

		fetchFollowers()
	}, [userId])

	if (loading) {
		return <p className="px-4 py-6 text-sm text-gray-400">Yükleniyor...</p>
	}

	if (users.length === 0) {
		return <p className="px-4 py-6 text-sm text-gray-400">Takipçi bulunamadı.</p>
	}

	return (
		<ul className="divide-y divide-neutral-800">
			{users.map((user) => (
				<li key={user.id} className="px-4 py-3 hover:bg-neutral-900/60">
					<Link href={`/profile?cameFrom=${user.id}`} className="block">
						<p className="font-semibold text-white">{user.display_name || user.username}</p>
						<p className="text-sm text-gray-400">@{user.username}</p>
					</Link>
				</li>
			))}
		</ul>
	)
}

