from django.urls import path
from . import views
app_name = 'resume'
urlpatterns = [
    path("managment/", views.PortfolioDashboardView.as_view(), name='resume_manager'),
    path("", views.test.as_view(), name='resume'),


]
