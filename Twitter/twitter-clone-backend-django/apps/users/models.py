from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from apps.common.models import TimeStampedModel, UUIDModel


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not username:
            raise ValueError("Username is required")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)


class User(UUIDModel, TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    display_name = models.CharField(max_length=60, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    avatar = models.URLField(blank=True)
    banner = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Follow(TimeStampedModel):
    follower = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["follower", "following"], name="unique_follow"),
        ]


class DirectConversation(UUIDModel, TimeStampedModel):
    user1 = models.ForeignKey(User, related_name="direct_conversations_as_user1", on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name="direct_conversations_as_user2", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user1", "user2"], name="unique_direct_conversation"),
        ]


class DirectMessage(UUIDModel, TimeStampedModel):
    conversation = models.ForeignKey(
        DirectConversation,
        related_name="messages",
        on_delete=models.CASCADE,
    )
    sender = models.ForeignKey(User, related_name="sent_direct_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_direct_messages", on_delete=models.CASCADE)
    text = models.TextField()
