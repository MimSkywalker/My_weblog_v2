from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.generic import DetailView, ListView, TemplateView
from django.views.generic.edit import FormMixin

from .forms import CommentForm
from .models import Category, Comment, Post, Tag
from resume.models import Profile


class BlogView(ListView):
    """

    """

    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 6
    MAX_FEATURED = 3

    def get_queryset(self):
        queryset = Post.objects.filter(status=Post.Status.PUBLISHED)

        self.search_query = self.request.GET.get('q', '').strip()
        self.category_slug = self.request.GET.get('category', '').strip()
        self.tag_slug = self.request.GET.get('tag', '').strip()
        self.is_filtered = bool(
            self.search_query or self.category_slug or self.tag_slug
        )

        if not self.is_filtered:
            queryset = queryset.filter(is_featured=False)

        if self.search_query:
            queryset = queryset.filter(
                Q(title__icontains=self.search_query)
                | Q(excerpt__icontains=self.search_query)
                | Q(content__icontains=self.search_query)
            )

        if self.category_slug:
            queryset = queryset.filter(categories__slug=self.category_slug)

        if self.tag_slug:
            queryset = queryset.filter(tags__slug=self.tag_slug)

        return (
            queryset.select_related('user')
            .prefetch_related('categories', 'tags')
            .distinct()
        )

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if is_ajax:
            paginator, page_obj, _, _ = self.paginate_queryset(
                self.object_list, self.get_paginate_by(self.object_list)
            )
            html = render_to_string(
                'blog/includes/_post_cards.html',
                {'posts': page_obj},
                request=request,
            )
            return JsonResponse({
                'html': html,
                'has_next': page_obj.has_next(),
                'next_page': (
                    page_obj.next_page_number() if page_obj.has_next() else None
                ),
                'count': paginator.count,
            })

        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['is_filtered'] = self.is_filtered
        context['search_query'] = self.search_query
        context['current_category'] = self.category_slug
        context['current_tag'] = self.tag_slug
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()

        context['featured_posts'] = (
            Post.objects.filter(
                status=Post.Status.PUBLISHED, is_featured=True
            )[:self.MAX_FEATURED]
            if not self.is_filtered
            else Post.objects.none()
        )

        context['total_posts_count'] = Post.objects.filter(
            status=Post.Status.PUBLISHED
        ).count()
        context['total_categories_count'] = Category.objects.count()

        return context


class BlogDetailView(FormMixin, DetailView):
    """

    """

    model = Post
    template_name = 'blog/blog-detail.html'
    context_object_name = 'post'
    form_class = CommentForm
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .select_related('user')
            .prefetch_related('categories', 'tags')
        )

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        context['profile'] = Profile.objects.first()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object

        parent_id = form.cleaned_data.get('parent_id')
        if parent_id:
            comment.parent = get_object_or_404(
                Comment, pk=parent_id, post=self.object
            )

        comment.save()
        messages.success(self.request, 'دیدگاه شما با موفقیت ثبت شد.')
        return super().form_valid(form)

    def form_invalid(self, form):
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def get_success_url(self):
        return reverse(
            'blog:blog-detail', kwargs={'slug': self.object.slug}
        ) + '#bdComments'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object

        context.setdefault('form', self.get_form())
        context['comment_form'] = context['form']

        context['comments'] = (
            post.comments.filter(parent__isnull=True)
            .select_related('post')
            .prefetch_related('replies')
        )

        related_qs = (
            Post.objects.filter(status=Post.Status.PUBLISHED)
            .exclude(pk=post.pk)
            .filter(
                Q(categories__in=post.categories.all())
                | Q(tags__in=post.tags.all())
            )
            .distinct()
        )
        context['related_posts'] = related_qs[:3]

        return context
