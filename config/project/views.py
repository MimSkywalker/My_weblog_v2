

from django.shortcuts import render
from .models import Project, Category, Technology
from django.views.generic import ListView, DetailView
from resume.models import Profile


class ProjectView(ListView):
    model = Project
    template_name = 'project/projects.html'
    paginate_by = 10
    paginate_orphans = 3
    context_object_name = 'projects'

    def get_queryset(self):
        context = super().get_queryset().prefetch_related('categories', 'technologies')

        category_slug = self.request.GET.get('category')
        if category_slug:
            context = context.filter(categories__slug=category_slug)
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['active_category'] = self.request.GET.get('category', '')
        context['profile'] = Profile.objects.first()

        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'
    context_object_name = 'project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_projects'] = (
            Project.objects
            .filter(categories__in=self.object.categories.all())
            .exclude(pk=self.object.pk)
            .distinct()[:3]
        )
        return context
