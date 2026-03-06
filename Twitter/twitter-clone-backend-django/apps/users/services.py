from apps.users.models import User


def register_user(*, email: str, username: str, password: str) -> User:
    return User.objects.create_user(email=email, username=username, password=password)
