from dataclasses import dataclass

from task_manager.domain.project.project import Project


@dataclass(frozen=True)
class ProjectDetail:
    project: Project
    total_estimation_project: int