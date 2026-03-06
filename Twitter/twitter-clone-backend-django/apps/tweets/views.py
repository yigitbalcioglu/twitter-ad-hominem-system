from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.common.pagination import DefaultPagination
from apps.common.permissions import IsOwnerOrReadOnly
from apps.tweets.models import Like, Retweet, Tweet
from apps.tweets.serializers import LikeSerializer, RetweetSerializer, TweetCreateSerializer, TweetSerializer
from apps.tweets.services import create_tweet, like_tweet, unlike_tweet


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.select_related("author").prefetch_related("media", "likes", "replies")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = DefaultPagination
    filterset_fields = {
        "author": ["exact", "in"],
        "reply_to": ["exact", "isnull"],
        "repost_of": ["exact", "isnull"],
    }
    search_fields = ["content"]

    def get_serializer_class(self):
        if self.action == "create":
            return TweetCreateSerializer
        if self.action in {"like", "unlike"}:
            return LikeSerializer
        return TweetSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tweet = create_tweet(author=request.user, **serializer.validated_data)
        output = TweetSerializer(tweet, context=self.get_serializer_context())
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        tweet = self.get_object()
        like = like_tweet(user=request.user, tweet=tweet)
        serializer = self.get_serializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        tweet = self.get_object()
        unlike_tweet(user=request.user, tweet=tweet)
        return Response(status=status.HTTP_204_NO_CONTENT)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.select_related("user", "tweet")
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filterset_fields = {
        "tweet": ["exact", "in"],
        "user": ["exact", "in"],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RetweetViewSet(viewsets.ModelViewSet):
    queryset = Retweet.objects.select_related("user", "tweet")
    serializer_class = RetweetSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = DefaultPagination
    filterset_fields = {
        "tweet": ["exact", "in"],
        "user": ["exact", "in"],
    }

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
