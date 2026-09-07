from django.contrib import admin
from .models import Project, Category, Technology


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'date_of_implementation')
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True
