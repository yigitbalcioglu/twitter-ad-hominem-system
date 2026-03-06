from rest_framework import serializers

from apps.users.models import DirectMessage, Follow, User


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "display_name",
            "bio",
            "location",
            "website",
            "avatar",
            "banner",
            "date_joined",
            "followers_count",
            "following_count",
            "is_following",
        )
        read_only_fields = ("id", "email", "date_joined")

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return Follow.objects.filter(follower=request.user, following=obj).exists()


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ("email", "username", "password")

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ("id", "follower", "following", "created_at")
        read_only_fields = ("id", "created_at")


class DirectMessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = DirectMessage
        fields = ("id", "conversation", "sender", "receiver", "text", "sender_username", "created_at")
        read_only_fields = ("id", "conversation", "sender", "receiver", "sender_username", "created_at")
