from task_manager.domain.project.project import Project
from task_manager.domain.project_detail.project_detail import ProjectDetail


class ProjectDetailCreator:
    def create(self, project: Project, total_estimation_project ) -> ProjectDetail:
        return ProjectDetail(project=project, total_estimation_project=total_estimation_project)