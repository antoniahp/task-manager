from uuid import UUID

from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_sprint_tasks.get_sprint_tasks_query import GetSprintTasksQuery
from task_manager.domain.exceptions.sprint_not_found_exception import SprintNotFoundException
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.sprint.sprint_repository import SprintRepository
from task_manager.domain.sprint_tasks.sprint_tasks_creator import SprintTasksCreator
from task_manager.domain.status_column.status_column_repository import StatusColumnRepository
from task_manager.domain.task.task_repository import TaskRepository
from task_manager.domain.user.user_repository import UserRepository


class GetSprintTasksQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository, status_column_repository: StatusColumnRepository, sprint_repository: SprintRepository, sprint_tasks_creator: SprintTasksCreator, user_repository: UserRepository):
        self.__task_repository = task_repository
        self.__status_column_repository = status_column_repository
        self.__sprint_repository = sprint_repository
        self.__sprint_tasks_creator = sprint_tasks_creator
        self.__user_repository = user_repository


    def handle(self, query: GetSprintTasksQuery) -> QueryResponse:
        requester_user = self.__user_repository.filter_user_by_id(user_id=query.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=query.requester_user_id)

        if not requester_user.belongs_to_company(company_id=query.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=query.requester_user_id, company_id=query.company_id)

        sprint = self.__sprint_repository.filter_sprint_by_id(sprint_id=query.sprint_id)
        if not sprint:
            raise SprintNotFoundException(sprint_id=query.sprint_id)

        tasks = self.__task_repository.filter_task(sprint_id=query.sprint_id)
        company_columns = self.__status_column_repository.filter_status_columns(company_id=UUID(str(sprint.company_id)))
        sprint_tasks = self.__sprint_tasks_creator.create(
            tasks=tasks,
            columns=company_columns
        )
        return QueryResponse(content=sprint_tasks)
