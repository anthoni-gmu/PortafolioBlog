from django.urls import path
from .views import ProjectHomeView
app_name="projects"

urlpatterns =[
    path('projects/',ProjectHomeView.as_view(),name="projects")
]