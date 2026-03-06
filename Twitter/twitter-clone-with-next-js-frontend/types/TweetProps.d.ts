type ITweetProps = {
    id: string;
    author: string;
    author_username?: string;
    content: string;
    reply_to: string | null;
    repost_of: string | null;
    is_ad_hominem?: boolean | null;
    ad_hominem_score?: number | null;
    ad_hominem_checked_at?: string | null;
    created_at: string;
    like_count?: number;
    reply_count?: number;
    retweet_count?: number;
};

