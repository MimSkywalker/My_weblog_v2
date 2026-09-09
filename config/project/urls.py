from django.urls import path
from . import views
app_name = 'project'
urlpatterns = [
    path("", views.ProjectView.as_view(), name='project'),
    path("<slug:slug>/", views.ProjectDetailView.as_view(), name='project_detail'),


]
