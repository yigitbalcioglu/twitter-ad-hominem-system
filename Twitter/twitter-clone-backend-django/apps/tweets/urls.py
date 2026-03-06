from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.tweets.views import LikeViewSet, RetweetViewSet, TweetViewSet

router = DefaultRouter()
router.register(r"tweets", TweetViewSet, basename="tweets")
router.register(r"likes", LikeViewSet, basename="likes")
router.register(r"retweets", RetweetViewSet, basename="retweets")

urlpatterns = [
    path("", include(router.urls)),
]
