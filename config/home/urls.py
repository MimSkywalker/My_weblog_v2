from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path("contact/", views.ContactView.as_view(), name='contact'),
    path("", views.IndexView.as_view(), name='index'),


]
