"use client"

import React, { useEffect, useMemo, useState } from 'react'
import { useSearchParams } from 'next/navigation'

interface IMessage {
    id: string;
    sender: string;
    receiver: string;
    text: string;
    sender_username: string;
    created_at: string;
}

export default function Page() {
    const [contacts, setContacts] = useState<IUserProps[]>([])
    const [selectedUserId, setSelectedUserId] = useState<string>("")
    const [messages, setMessages] = useState<IMessage[]>([])
    const [text, setText] = useState<string>("")
    const [socket, setSocket] = useState<WebSocket | null>(null)
    const searchParams = useSearchParams()
    const userFromQuery = searchParams.get("to") ?? ""

    useEffect(() => {
        const fetchContacts = async () => {
            const response = await fetch("/api/messages/contacts", {
                method: "GET",
            })

            if (!response.ok) {
                setContacts([])
                return
            }

            const data = await response.json()
            const users = Array.isArray(data?.results) ? data.results : data
            setContacts(users)

            if (userFromQuery && users.find((user: IUserProps) => user.id === userFromQuery)) {
                setSelectedUserId(userFromQuery)
                return
            }

            if (!selectedUserId && users.length > 0) {
                setSelectedUserId(users[0].id)
            }
        }

        fetchContacts()
    }, [selectedUserId, userFromQuery])

    useEffect(() => {
        const fetchMessages = async () => {
            if (!selectedUserId) {
                setMessages([])
                return
            }

            const response = await fetch(`/api/messages/${selectedUserId}`, {
                method: "GET",
            })

            if (!response.ok) {
                setMessages([])
                return
            }

            const data = await response.json()
            setMessages(Array.isArray(data) ? data : [])
        }

        fetchMessages()
    }, [selectedUserId])

    useEffect(() => {
        if (!selectedUserId) {
            if (socket) {
                socket.close()
                setSocket(null)
            }
            return
        }

        const wsBaseUrl = process.env.NEXT_PUBLIC_WS_BASE_URL ?? "ws://localhost:8000"
        const ws = new WebSocket(`${wsBaseUrl}/ws/messages/${selectedUserId}/`)

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data) as IMessage
                setMessages((prev) => [...prev, data])
            } catch (error) {
                return
            }
        }

        setSocket(ws)

        return () => {
            ws.close()
            setSocket(null)
        }
    }, [selectedUserId])

    const activeContact = useMemo(
        () => contacts.find((contact) => contact.id === selectedUserId),
        [contacts, selectedUserId]
    )

    const sendMessage = async () => {
        const content = text.trim()
        if (!selectedUserId || !content || !socket || socket.readyState !== WebSocket.OPEN) {
            return
        }

        socket.send(JSON.stringify({ text: content }))
        setText("")
    }

    return (
        <div className='text-white min-h-[70vh] md:grid md:grid-cols-3'>
            <div className='border-b border-neutral-800 p-3 md:border-b-0 md:border-r'>
                <h2 className='font-bold mb-3'>Takip Ettiklerim</h2>
                <div className='flex gap-2 overflow-x-auto pb-1 md:block md:space-y-2 md:overflow-visible md:pb-0'>
                    {contacts.map((contact) => (
                        <button
                            key={contact.id}
                            onClick={() => setSelectedUserId(contact.id)}
                            className={`shrink-0 rounded-xl px-3 py-2 text-left whitespace-nowrap md:w-full ${selectedUserId === contact.id ? "bg-neutral-800" : "bg-neutral-900"}`}
                        >
                            @{contact.username}
                        </button>
                    ))}
                </div>
            </div>

            <div className='p-3 flex flex-col md:col-span-2'>
                <h2 className='font-bold mb-3'>
                    {activeContact ? `@${activeContact.username} ile mesajlar` : "Mesajlaşmak için kullanıcı seç"}
                </h2>

                <div className='flex-1 overflow-y-auto space-y-2 mb-3'>
                    {messages.map((message) => (
                        <div key={message.id} className='bg-neutral-900 rounded-xl p-3'>
                            <p className='text-sm text-gray-400 mb-1'>@{message.sender_username}</p>
                            <p>{message.text}</p>
                        </div>
                    ))}
                </div>

                <div className='flex gap-2'>
                    <input
                        value={text}
                        onChange={(event) => setText(event.target.value)}
                        placeholder='Mesaj yaz...'
                        className='flex-1 rounded-xl bg-neutral-900 px-3 py-2 outline-none border border-neutral-800'
                    />
                    <button
                        onClick={sendMessage}
                        className='bg-[#009CFF] rounded-xl px-3 py-2 text-sm sm:px-4'
                    >
                        Gönder
                    </button>
                </div>
            </div>
        </div>
    )
}
