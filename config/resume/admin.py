from django.contrib import admin
from .models import Profile, Experience, Skill, Education, SocialLink, Expertise


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'projects_count', 'phone_number')
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date')
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True
    search_fields = ['name']


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('institution', 'field_of_study',
                    'degree', 'start_date', 'end_date')
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    list_display = ('title', 'score')
    readonly_fields = ['updated_at', 'created_at']
    date_hierarchy = 'created_at'
    save_on_top = True
