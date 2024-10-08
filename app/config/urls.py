"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ninja_jwt.controller import NinjaJWTDefaultController
from ninja_extra import NinjaExtraAPI


from task_manager.infrastructure.companies.company_views import company_router
from task_manager.infrastructure.projects.project_views import project_router
from task_manager.infrastructure.status_columns.status_columns_views import status_columns_router
from task_manager.infrastructure.task.task_views import task_router
from task_manager.infrastructure.sprints.sprints_views import sprint_router
from task_manager.infrastructure.user_story.user_story_views import user_story_router
from task_manager.infrastructure.users.user_views import user_router


api = NinjaExtraAPI()
api.register_controllers(NinjaJWTDefaultController)

api.add_router("/users/", user_router)
api.add_router("/company/", company_router)
api.add_router("/projects/", project_router)
api.add_router("/sprints/", sprint_router)
api.add_router("/user-story/", user_story_router)
api.add_router("/tasks/", task_router)
api.add_router("/status-columns/", status_columns_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
]
