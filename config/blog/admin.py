from django.contrib import admin
from .models import Post, Category, Tag, Comment

from django.utils.html import format_html
from .models import Post, Category, Tag, Comment, PostImage, FAQ
from .forms import PostAdminForm


class PostImageInline(admin.TabularInline):
    model = PostImage
    extra = 3
    fields = ['image', 'caption', 'preview', 'copy_tag']
    readonly_fields = ['preview', 'copy_tag']

    def preview(self, obj):
        if obj.pk and obj.image:
            return format_html(
                '<img src="{}" style="max-height:80px;border-radius:6px;">',
                obj.image.url,
            )
        return '—'
    preview.short_description = 'پیش‌نمایش'

    def copy_tag(self, obj):
        if obj.pk:
            return format_html('<code>{}</code>', obj.markdown_tag)
        return 'بعد از ذخیره نمایش داده می‌شه'
    copy_tag.short_description = 'کد جایگذاری در مارک‌داون'

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ['order', 'question', 'answer']
    ordering = ['order']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    inlines = [PostImageInline, FAQInline]
    list_display = ['title', 'slug', 'status', 'published_at', 'is_featured']
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'parent', 'full_name', 'created_at']
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True
