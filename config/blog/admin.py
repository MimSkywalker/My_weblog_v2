from django.contrib import admin
from .models import Post, Category, Tag, Comment


@admin.register(Post)
class PostAdmoin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status', 'published_at', "is_featured"]
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True
    list_display = ("is_featured",'status',)


@admin.register(Category)
class CategoryAdmoin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Tag)
class TagAdmoin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Comment)
class CommentAdmoin(admin.ModelAdmin):
    list_display = ['post', 'parent', 'full_name', 'created_at']
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True
