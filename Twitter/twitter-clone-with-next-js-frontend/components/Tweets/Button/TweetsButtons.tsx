"use client"

import React, { useState, useEffect, useRef } from 'react'
import { FaRegComment, FaRetweet } from 'react-icons/fa';
import { CommentModal } from '../../Modal/CommentModal';
import { handleLike, handleRemoveLike } from '../handleButtons/handleLikeClick';
import { useRouter } from 'next/navigation';
import useSWR, { mutate } from 'swr';
import { handleRetweet, handleRemoveRetweet } from '../Retweet/handleRetweet';

interface ITweetsButtonsProps {
    currentUserId: string
    post: ITweetProps
    user: IUserProps
    commentLength: number
    whosLikedTweet: string[]
    retweetLenght: number
}

const TweetsButtons = ({ currentUserId, post, user, commentLength, whosLikedTweet, retweetLenght }: ITweetsButtonsProps) => {

    const [commentClick, setCommentClick] = useState<boolean>(false);
    const [isModalOpen, setIsModalOpen] = useState<boolean>(false)
    const [likeState, setLikeState] = useState<boolean>(whosLikedTweet.includes(currentUserId));
    const [retweetState, setSetRetweet] = useState<boolean>(false);
    const [showDropdown, setShowDropdown] = useState<boolean>(false);

    const dropdownRef = useRef<HTMLDivElement>(null);
    const modalRef = useRef<HTMLDivElement>(null);

    const handleCommentClick = () => {
        setIsModalOpen(true);
        setCommentClick(true);
    };

    const closeModal = () => {
        setIsModalOpen(false);
        setCommentClick(false);
    };

    const handleRetweetClick = () => {
        !showDropdown && setShowDropdown(true); // Dropdown'u aç/kapa
    };

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setShowDropdown(false); // Dropdown dışına tıklandığında kapat
            }

            if (modalRef.current && !modalRef.current.contains(event.target as Node)) {
                closeModal(); // Modal dışına tıklandığında kapat
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, []);

    async function handleLikeClick() {
        setLikeState(!likeState);

        if (likeState) {
            // Remove like if already liked
            await handleRemoveLike(currentUserId, post.id);
        } else {
            // Add like if not already liked
            await handleLike(currentUserId, post.id);
        }

    }

    return (

        <>
            <div className='border-b-2 border-neutral-800'>
                <div className='ml-0 grid grid-cols-3 gap-2 pb-2 pt-2 text-gray-500 sm:ml-[3.25rem]'>
                    {showDropdown
                        ? (
                            <div ref={dropdownRef} className="rounded-3xl border border-gray-300 bg-black shadow-md shadow-white">
                                <ul className="text-white ml-2">
                                    <li className="flex px-4 pt-2 hover:bg-gray-900 hover:rounded-t-3xl cursor-pointer"><FaRetweet
                                        size={20}
                                    />Yeniden gönder</li>
                                    <li className="px-4 py-2 hover:bg-gray-900 cursor-pointer">Alıntı</li>
                                    <li className="px-4 pb-2 hover:bg-gray-900 hover:rounded-b-3xl cursor-pointer">Alıntılar görüntüle</li>
                                </ul>
                            </div>
                        ) :
                        <div className='flex items-center gap-2'>

                            <FaRegComment size={20} onClick={handleCommentClick} />
                            <p>{commentLength}</p>

                        </div>
                    }

                    <div className='flex items-center gap-2'>

                        <FaRetweet
                            size={20}
                            onClick={handleRetweetClick} />
                        <p>{retweetLenght}</p>

                    </div>

                    <div className='relative flex items-center'
                        onClick={handleLikeClick}
                        id="heart-container">
                        <input
                            type="checkbox"
                            id="toggle"
                            className="absolute opacity-0 scale-150"
                            checked={likeState}
                            onChange={() => { }} />
                        <div id="twitter-heart"
                            className={`absolute pointer-events-none bg-[url('https://abs.twimg.com/a/1454637594/img/t1/web_heart_animation.png')] bg-no-repeat h-24 w-24 -top-10 -left-10 ${likeState ? 'animate-heart' : ''
                                }`}></div><p className='ml-8 text-white'>{whosLikedTweet.length}</p>
                    </div>
                </div>

            </div>
            {isModalOpen && commentClick && (
                <div ref={modalRef}>
                    <CommentModal user={user} currentUserId={currentUserId} post={post} closeModal={closeModal} />
                </div>
            )}
        </>

    )
}

export default TweetsButtons