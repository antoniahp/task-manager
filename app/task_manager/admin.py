from django.contrib import admin

from task_manager.domain.company.company import Company
from task_manager.domain.project.project import Project
from task_manager.domain.sprint.sprint import Sprint
from task_manager.domain.status_column.status_column import StatusColumn
from task_manager.domain.task.task import Task
from task_manager.domain.user.user import User
from task_manager.domain.user_story.user_story import UserStory


class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "start_date",
        "end_date",
    ]

class SprintAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "start_date",
        "end_date",
        "active",
    ]

class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "estimation",
        "completed",
    ]

class StatusColumnAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]

class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
    ]



admin.site.register(Project, ProjectAdmin)
admin.site.register(Sprint, SprintAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(StatusColumn, StatusColumnAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserStory)


