from cqrs.commands.command_handler import CommandHandler
from task_manager.application.create_user_story.create_user_story_command import CreateUserStoryCommand
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.user.user_repository import UserRepository
from task_manager.domain.user_story.user_story_creator import UserStoryCreator
from task_manager.domain.user_story.user_story_repository import UserStoryRepository


class CreateUserStoryCommandHandler(CommandHandler):
    def __init__(self, user_story_creator: UserStoryCreator, user_story_repository: UserStoryRepository, user_repository: UserRepository):
        self.__user_story_creator = user_story_creator
        self.__user_story_repository = user_story_repository
        self.__user_repository = user_repository

    def handle(self, command: CreateUserStoryCommand):
        requester_user = self.__user_repository.filter_user_by_id(user_id=command.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=command.requester_user_id)

        if not requester_user.belongs_to_company(company_id=command.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=command.requester_user_id, company_id=command.company_id)


        user_story = self.__user_story_creator.create_user_story(
            user_story_id=command.user_story_id,
            title=command.title,
            description=command.description,
            estimation=command.estimation,
            completed=command.completed,
            project_id=command.project_id,
            assigned_user_id=command.assigned_user_id,
            status_column_id=command.status_column_id,
            completed_at=command.completed_at
        )
        self.__user_story_repository.save_user_story(user_story)