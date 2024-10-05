from uuid import UUID


class UserStoryNotFoundException(Exception):
    def __init__(self, user_story_id: UUID):
        self.user_story_id = user_story_id
        self.message = f"User Story {user_story_id} not found"
        super().__init__(self.message)