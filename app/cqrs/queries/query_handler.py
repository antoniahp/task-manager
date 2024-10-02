from abc import ABC, abstractmethod
from cqrs.queries.query import Query
from cqrs.queries.query_response import QueryResponse


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> QueryResponse:
        pass