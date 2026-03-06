from rest_framework import serializers

from apps.tweets.models import Like, Retweet, Tweet, TweetMedia


class TweetMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetMedia
        fields = ("id", "url", "media_type")
        read_only_fields = ("id",)


class TweetSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source="author.username", read_only=True)
    media = TweetMediaSerializer(many=True, read_only=True)
    like_count = serializers.IntegerField(source="likes.count", read_only=True)
    reply_count = serializers.IntegerField(source="replies.count", read_only=True)
    retweet_count = serializers.IntegerField(source="retweets.count", read_only=True)

    class Meta:
        model = Tweet
        fields = (
            "id",
            "author",
            "author_username",
            "content",
            "reply_to",
            "repost_of",
            "is_ad_hominem",
            "ad_hominem_score",
            "ad_hominem_checked_at",
            "created_at",
            "media",
            "like_count",
            "reply_count",
            "retweet_count",
        )
        read_only_fields = (
            "id",
            "author",
            "created_at",
            "is_ad_hominem",
            "ad_hominem_score",
            "ad_hominem_checked_at",
        )


class TweetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ("content", "reply_to", "repost_of")

    def validate(self, attrs):
        if attrs.get("reply_to") and attrs.get("repost_of"):
            raise serializers.ValidationError("A tweet cannot be both a reply and a repost.")
        return attrs


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ("id", "user", "tweet", "created_at")
        read_only_fields = ("id", "created_at", "user")


class RetweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Retweet
        fields = ("id", "user", "tweet", "created_at")
        read_only_fields = ("id", "created_at", "user")
