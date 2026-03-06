import { Comment } from './Comment';
import getPhoto from '@/hooks/getPhoto';

interface PostProp {
    comments: ITweetProps[] | null
    users: IUserProps[]
    currentUserId: string
    whosLikedTweet: LikeProp[]
    post: ITweetProps
    secondaryComments: ITweetProps[] | null
    retweets: LikeProp[] | null
}

export const RelatedComments = async ({ currentUserId, post, comments, users, whosLikedTweet, secondaryComments, retweets }: PostProp) => {

    return (
        <div>
            {comments && comments.length > 0 ?
                (
                    <ul>
                        {comments.map(async (comment) => {
                            const usersWhoLikedTweet = whosLikedTweet.filter(like => like.tweet === comment.id).map(e => e.user)
                            const tweetOwner = users.find(user => user.id === comment.author)
                            const photoUrl = await getPhoto(tweetOwner?.id!);

                            const commentsOfComments = secondaryComments?.filter(secondaryComment => secondaryComment.reply_to === comment.id)

                            return (
                                <li key={comment.id}>
                                    <div className=' hover:bg-gray-950'>
                                        <Comment
                                            currentUserId={currentUserId}
                                            post={comment}
                                            user={tweetOwner!}
                                            photo={photoUrl}
                                            comments={commentsOfComments}
                                            whosLikedTweet={usersWhoLikedTweet}
                                        />
                                    </div>
                                </li>
                            )
                        })}
                    </ul>
                ) : (
                    <p>{null}</p>
                )
            }
        </div >

    )
}



