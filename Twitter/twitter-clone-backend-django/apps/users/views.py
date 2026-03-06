from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.models import DirectConversation, DirectMessage, Follow, User
from apps.users.serializers import DirectMessageSerializer, UserCreateSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserCreateSerializer


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = {
        "id": ["exact", "in"],
        "username": ["exact", "in"],
    }


class FollowToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        if target_user.id == request.user.id:
            return Response({"detail": "Kendini takip edemezsin."}, status=status.HTTP_400_BAD_REQUEST)

        follow = Follow.objects.filter(follower=request.user, following=target_user).first()
        if follow:
            follow.delete()
            return Response({"following": False}, status=status.HTTP_200_OK)

        Follow.objects.create(follower=request.user, following=target_user)
        return Response({"following": True}, status=status.HTTP_201_CREATED)


class FollowStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        target_id = request.query_params.get("user_id")
        if not target_id:
            return Response({"detail": "user_id zorunludur."}, status=status.HTTP_400_BAD_REQUEST)

        target_user = get_object_or_404(User, id=target_id)
        is_following = Follow.objects.filter(follower=request.user, following=target_user).exists()
        return Response({"following": is_following}, status=status.HTTP_200_OK)


class FollowingListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        target_id = self.request.query_params.get("user_id")
        target_user = self.request.user

        if target_id:
            target_user = get_object_or_404(User, id=target_id)

        followed_ids = Follow.objects.filter(follower=target_user).values_list("following_id", flat=True)
        return User.objects.filter(id__in=followed_ids)


class FollowersListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        target_id = self.request.query_params.get("user_id")
        target_user = self.request.user

        if target_id:
            target_user = get_object_or_404(User, id=target_id)

        follower_ids = Follow.objects.filter(following=target_user).values_list("follower_id", flat=True)
        return User.objects.filter(id__in=follower_ids)


class DirectMessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def _get_or_create_conversation(self, user_a, user_b):
        ordered = sorted([user_a, user_b], key=lambda user: str(user.id))
        conversation, _ = DirectConversation.objects.get_or_create(user1=ordered[0], user2=ordered[1])
        return conversation

    def _can_message(self, request_user, target_user):
        return Follow.objects.filter(follower=request_user, following=target_user).exists()

    def get(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        if target_user.id == request.user.id:
            return Response({"detail": "Kendine mesaj atamazsın."}, status=status.HTTP_400_BAD_REQUEST)

        if not self._can_message(request.user, target_user):
            return Response(
                {"detail": "Sadece takip ettiğin kullanıcılara mesaj atabilirsin."},
                status=status.HTTP_403_FORBIDDEN,
            )

        conversation = self._get_or_create_conversation(request.user, target_user)
        messages = DirectMessage.objects.filter(conversation=conversation).order_by("created_at")
        serializer = DirectMessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        target_user = get_object_or_404(User, id=user_id)
        if target_user.id == request.user.id:
            return Response({"detail": "Kendine mesaj atamazsın."}, status=status.HTTP_400_BAD_REQUEST)

        if not self._can_message(request.user, target_user):
            return Response(
                {"detail": "Sadece takip ettiğin kullanıcılara mesaj atabilirsin."},
                status=status.HTTP_403_FORBIDDEN,
            )

        text = (request.data.get("text") or "").strip()
        if not text:
            return Response({"detail": "Mesaj boş olamaz."}, status=status.HTTP_400_BAD_REQUEST)

        conversation = self._get_or_create_conversation(request.user, target_user)
        message = DirectMessage.objects.create(
            conversation=conversation,
            sender=request.user,
            receiver=target_user,
            text=text,
        )
        serializer = DirectMessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageContactsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_ids = Follow.objects.filter(follower=self.request.user).values_list("following_id", flat=True)
        conversation_partner_ids = DirectConversation.objects.filter(
            Q(user1=self.request.user) | Q(user2=self.request.user)
        ).values_list("user1_id", "user2_id")

        partner_ids = set()
        for user1_id, user2_id in conversation_partner_ids:
            if user1_id == self.request.user.id:
                partner_ids.add(user2_id)
            else:
                partner_ids.add(user1_id)

        combined_ids = set(following_ids) | partner_ids
        return User.objects.filter(id__in=combined_ids)
