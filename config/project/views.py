from django.shortcuts import render
from .models import Project, Category, Technology
from django.views.generic import ListView


class ProjectView(ListView):
    model = Project
    template_name = 'project/projects.html'
