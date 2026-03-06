"use client"

import React, { useState, useEffect } from 'react';
import { useFormik } from "formik";
import { Avatar } from '../Image/Avatar';
import { useRouter } from 'next/navigation';

interface CommentModalProps {
    post: ITweetProps;
    closeModal: () => void;// Add closeModal prop
    currentUserId: string
    user: IUserProps
}

export const CommentModal: React.FC<CommentModalProps> = ({ post, user, closeModal, currentUserId }) => {
    const [formData, setFormData] = useState({
        body: "",
        isLoading: false,
        disabled: true,
    });

    const month = new Date(post.created_at).getMonth()
    const year = new Date(post.created_at).getFullYear()

    const router = useRouter()

    useEffect(() => {
        setFormData(prev => ({
            ...prev,
            disabled: formData.body.trim() === "",
        }));
    }, [formData.body]);

    const formik = useFormik({
        initialValues: {
            text: ""
        },
        onSubmit: async (values, { resetForm }) => {
            setFormData(prev => ({ ...prev, isLoading: true }));
            try {
                const sessionResponse = await fetch('/api/comments/sendComment', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        parent: post.id,
                        tweet: formData.body,
                    }),
                });

                if (!sessionResponse.ok) {
                    throw new Error("Response failed");
                } else {
                    resetForm();
                    setFormData(prev => ({ ...prev, body: "" }));
                }
            } catch (error) {
                console.error(error);
            } finally {
                setFormData(prev => ({ ...prev, isLoading: false }));
                router.refresh()
            }
        }
    });

    return (
        <form onSubmit={formik.handleSubmit}>
            <div className="fixed inset-0 z-10 flex items-start justify-center bg-white bg-opacity-30">
                <div className="bg-black text-white p-4 rounded-lg max-w-lg w-full">
                    <div className="flex justify-between items-center">
                        <button type="button" onClick={closeModal} className="text-gray-400 hover:text-gray-200">&times;</button>
                    </div>
                    <div className="cursor-pointer">
                        <div className='flex'>
                            <Avatar
                                ownersId={post.author}
                            />
                            <div className='w-full'>
                                <div className='flex'>
                                    <p className='text-white mt-1 font-semibold'>{user?.display_name ?? user?.username ?? 'Bilinmeyen Kullanici'}</p>
                                    <p className='text-gray-500 mt-1 pl-1'>@{user?.username ?? 'unknown'}</p>
                                    <p className='text-gray-500 pl-1'>.</p>
                                    <p className='text-gray-500 mt-1 pl-1'>{month}</p>
                                    <p className='text-gray-500 mt-1 pl-1'>{year}</p>
                                </div>
                                <p className='text-white'>{post.content}</p>
                                <p className='text-gray-500 mt-3 pl-1'>
                                    <span className='text-blue-400'>@{user?.username ?? 'unknown'}</span> adlı kullanıcıya yanıt olarak
                                </p>
                            </div>
                        </div>
                        <div className='flex mt-3'>
                            <Avatar
                                ownersId={currentUserId}
                            />
                            <div className='w-full'>
                                <textarea
                                    disabled={formData.isLoading}
                                    onChange={(e) => setFormData(prev => ({ ...prev, body: e.target.value }))}
                                    value={formData.body}
                                    className='disabled:opacity-50
                                    peer
                                    resize-none
                                    mt-3
                                    ml-1
                                    w-full
                                    bg-black
                                    ring-0
                                    outline-none
                                    text-[20px]
                                    placeholder-neutral-500
                                    text-white'
                                    placeholder="Yanıtını gönder"
                                ></textarea>
                                <div className="mt-2 flex flex-row justify-end">
                                    <button
                                        className={`bg-[#009CFF] rounded-3xl w-24 h-9 ${formData.disabled ? "opacity-50" : "opacity-100"}`}
                                        type="submit"
                                        disabled={formData.disabled || formData.isLoading}>
                                        Yanıtla
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </form>
    );
};