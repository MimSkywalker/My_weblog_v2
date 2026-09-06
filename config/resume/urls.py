from django.urls import path
from . import views
app_name = 'resume'
urlpatterns = [
    path("managment/", views.PortfolioDashboardView.as_view(), name='resume_manager'),
    path("", views.test.as_view(), name='resume_manager'),
    path("1", views.test1.as_view(), name='resume_manager'),
    path("2", views.test2.as_view(), name='resume_manager'),
    path("3", views.test3.as_view(), name='resume_manager'),






]
