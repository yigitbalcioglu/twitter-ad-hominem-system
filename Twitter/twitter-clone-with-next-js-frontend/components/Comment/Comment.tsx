"use client"

import { useRouter } from 'next/navigation';
import { ProfilePhoto } from '../Image/ProfilePhoto';
import Post from '../Tweets/Tweet Component/Post';
import TweetsButtons from '../Tweets/Button/TweetsButtons';

interface PostsListProps {
    post: ITweetProps
    currentUserId: string
    user: IUserProps
    photo: string
    whosLikedTweet: string[]
    comments: ITweetProps[] | null
}

export const Comment: React.FC<PostsListProps> = ({ post, currentUserId, user, photo, whosLikedTweet, comments }) => {

    return (
        <>
            <div className="flex cursor-pointer pb-4" >

                <ProfilePhoto
                    ownerId={post.author}
                    photo={photo}
                />
                <Post
                    user={user}
                    post={post} />
            </div>

            <TweetsButtons
                currentUserId={currentUserId}
                post={post}
                user={user}
                commentLength={comments?.length}
                whosLikedTweet={whosLikedTweet}
                retweetLenght={0}
            />
        </>
    )
}