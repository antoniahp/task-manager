from ninja import Schema

from task_manager.infrastructure.projects.get_project_schema import GetProjectSchema


class GetProjectDetailSchema(Schema):
    project: GetProjectSchema
    total_estimation_project: int
