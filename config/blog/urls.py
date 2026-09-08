from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path("", views.BlogView.as_view(), name='blog'),
    path("1", views.BlogDetailView.as_view(), name='blog-detail'),


]
