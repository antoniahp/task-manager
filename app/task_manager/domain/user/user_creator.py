from uuid import UUID

from task_manager.domain.user.user import User


class UserCreator:
    def create_user(self, user_id: UUID, name:str, username: str, password: str, email: str) -> User:
        return User(
            id=user_id,
            name=name,
            username=username,
            password=password,
            email=email
        )
