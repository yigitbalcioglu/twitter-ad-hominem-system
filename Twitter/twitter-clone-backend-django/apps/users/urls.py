from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import (
    DirectMessageView,
    FollowersListView,
    FollowStatusView,
    FollowToggleView,
    FollowingListView,
    MeView,
    MessageContactsView,
    RegisterView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("me/", MeView.as_view(), name="me"),
    path("follows/status/", FollowStatusView.as_view(), name="follow_status"),
    path("follows/following/", FollowingListView.as_view(), name="following_list"),
    path("follows/followers/", FollowersListView.as_view(), name="followers_list"),
    path("follows/<uuid:user_id>/toggle/", FollowToggleView.as_view(), name="follow_toggle"),
    path("messages/contacts/", MessageContactsView.as_view(), name="message_contacts"),
    path("messages/<uuid:user_id>/", DirectMessageView.as_view(), name="direct_messages"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]
