from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class DirectMessageConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        user = self.scope.get("user")
        if not user or not user.is_authenticated:
            await self.close(code=4401)
            return

        self.current_user = user
        self.target_user_id = str(self.scope["url_route"]["kwargs"]["user_id"])

        if str(self.current_user.id) == self.target_user_id:
            await self.close(code=4400)
            return

        target_user = await self._get_target_user(self.target_user_id)
        if not target_user:
            await self.close(code=4404)
            return

        self.target_user = target_user
        can_message = await self._can_message(self.current_user.id, self.target_user.id)
        if not can_message:
            await self.close(code=4403)
            return

        self.group_name = self._conversation_group_name(str(self.current_user.id), str(self.target_user.id))

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        text = (content.get("text") or "").strip()
        if not text:
            return

        message = await self._create_message(self.current_user.id, self.target_user.id, text)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message": {
                    "id": str(message.id),
                    "sender": str(message.sender_id),
                    "receiver": str(message.receiver_id),
                    "text": message.text,
                    "sender_username": self.current_user.username,
                    "created_at": message.created_at.isoformat(),
                },
            },
        )

    async def chat_message(self, event):
        await self.send_json(event["message"])

    def _conversation_group_name(self, user_id_1, user_id_2):
        ordered = sorted([user_id_1, user_id_2])
        return f"direct_chat_{ordered[0]}_{ordered[1]}"

    @database_sync_to_async
    def _get_target_user(self, target_user_id):
        from apps.users.models import User

        return User.objects.filter(id=target_user_id).first()

    @database_sync_to_async
    def _can_message(self, current_user_id, target_user_id):
        from apps.users.models import Follow

        return Follow.objects.filter(follower_id=current_user_id, following_id=target_user_id).exists()

    @database_sync_to_async
    def _create_message(self, sender_id, receiver_id, text):
        from apps.users.models import DirectConversation, DirectMessage

        ordered_ids = sorted([str(sender_id), str(receiver_id)])
        conversation, _ = DirectConversation.objects.get_or_create(
            user1_id=ordered_ids[0],
            user2_id=ordered_ids[1],
        )
        return DirectMessage.objects.select_related("sender").create(
            conversation=conversation,
            sender_id=sender_id,
            receiver_id=receiver_id,
            text=text,
        )
