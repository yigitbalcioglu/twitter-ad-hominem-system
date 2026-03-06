import { verifySession } from "@/lib/dal";
import { FetchTweets } from "@/hooks/fetchTweets";
import fetchRelatedUsers from "@/hooks/fetchTweetsUsers";
import HomePageTweets from "@/components/Tweets/Home Page/HomePageTweets";
import getPhoto from "@/hooks/getPhoto";
import SendPost from "@/components/Tweets/Send Tweet/SendPost";
import fetchRelatedUrls from "@/hooks/fetchPhotoUrls";
import { fetchLikes } from "@/hooks/fetchLikes";
import { getHomePageComments } from "@/hooks/getComments";

export default async function Home() {
    const session = await verifySession();
    const tweets = (await FetchTweets(10)) as ITweetProps[];
    const id = session.userId;
    const users = (await fetchRelatedUsers(tweets)) ?? [];
    const urls = await fetchRelatedUrls(users);
    const url = await getPhoto(id);
    const likes = (await fetchLikes(tweets)) ?? [];
    const comments = (await getHomePageComments(tweets)) ?? [];

    return (
        <div className="text-white">
            <SendPost mode="Tweet" userId={id} photoUrl={url} />

            <HomePageTweets
                userId={id}
                tweets={tweets}
                users={users}
                urls={urls}
                likes={likes}
                comments={comments}
            />
        </div>
    );
}
