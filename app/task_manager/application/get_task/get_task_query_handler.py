from cqrs.queries.query_handler import QueryHandler
from cqrs.queries.query_response import QueryResponse
from task_manager.application.get_task.get_task_query import GetTaskQuery
from task_manager.domain.exceptions.user_does_not_belong_to_company_exception import UserDoesNotBelongToCompanyException
from task_manager.domain.exceptions.user_not_found_exception import UserNotFoundException
from task_manager.domain.task.task_repository import TaskRepository
from task_manager.domain.user.user_repository import UserRepository


class GetTaskQueryHandler(QueryHandler):
    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.__task_repository = task_repository
        self.__user_repository = user_repository

    def handle(self, query: GetTaskQuery) -> QueryResponse:
        requester_user = self.__user_repository.filter_user_by_id(user_id=query.requester_user_id)
        if requester_user is None:
            raise UserNotFoundException(user_id=query.requester_user_id)

        if not requester_user.belongs_to_company(company_id=query.company_id):
            raise UserDoesNotBelongToCompanyException(requester_user_id=query.requester_user_id, company_id=query.company_id)

        tasks = self.__task_repository.filter_task(task_id=query.task_id, title=query.title, estimation=query.estimation, completed=query.completed, sprint_id=query.sprint, assigned_user_id=query.assigned_user_id, status_column_id=query.status_column_id, user_story_id=query.user_story_id, completed_at=query.completed_at, completed_at__lte=query.completed_at__lte, completed_at__gte=query.completed_at__gte, deleted=query.deleted, company_id=query.company_id)
        return QueryResponse(content=tasks)