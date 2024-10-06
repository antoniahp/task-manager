from uuid import UUID


class UserNotFoundException(Exception):
    def __init__(self, user_id: UUID):
        self.user_id = user_id
        self.message = f"User {user_id} not found"
        super().__init__(self.message)