from cqrs.commands.command_handler import CommandHandler
from task_manager.application.update_user_story.update_user_story_command import UpdateUserStoryCommand
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.exceptions.user_story_not_found_exception import UserStoryNotFoundException
from task_manager.domain.user.user_repository import UserRepository
from task_manager.domain.user_story.user_story_repository import UserStoryRepository



class UpdateUserStoryCommandHandler(CommandHandler):
    def __init__(self, user_story_repository:UserStoryRepository, user_repository:UserRepository):
        self.__user_story_repository = user_story_repository
        self.__user_repository = user_repository

    def handle(self, command: UpdateUserStoryCommand):
        requester_user = self.__user_repository.filter_user_by_id(user_id=command.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=command.requester_user_id)

        if not requester_user.belongs_to_company(company_id=command.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=command.requester_user_id, company_id=command.company_id)
        user_story_filtered = self.__user_story_repository.filter_user_story_by_id(user_story_id=command.user_story_id)
        if user_story_filtered is None:
            raise UserStoryNotFoundException(user_story_id=command.user_story_id)

        user_story_filtered.title = command.title
        user_story_filtered.description = command.description
        user_story_filtered.estimation = command.estimation
        user_story_filtered.completed = command.completed
        user_story_filtered.project_id= command.project_id
        user_story_filtered.assigned_user_id= command.assigned_user_id
        user_story_filtered.status_column_id= command.status_column_id

        self.__user_story_repository.save_user_story(user_story_filtered)
