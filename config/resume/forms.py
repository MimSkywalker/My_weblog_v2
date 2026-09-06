from django import forms
from django.forms import modelformset_factory
from .models import Profile, Experience, Skill, Education, SocialLink, Expertise


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'first_name', 'last_name', 'bio',
                  'years_of_experience', 'projects_count', 'resume_file', 'email', 'phone_number']


ExperienceFormSet = modelformset_factory(
    Experience,
    fields=['title', 'start_date', 'end_date', 'description'],
    extra=1,
    can_delete=True,
    can_order=True
)

SkillFormSet = modelformset_factory(
    Skill,
    fields=['name', 'description'],
    extra=1,
    can_delete=True,
    can_order=True
)


EducationFormSet = modelformset_factory(
    Education,
    fields=['institution', 'field_of_study', 'degree',
            'description', 'start_date', 'end_date'],
    extra=1,
    can_delete=True,
    can_order=True
)

ExpertiseFormSet = modelformset_factory(
    Expertise,
    fields=['title', 'score'],
    extra=1,
    can_delete=True,
    can_order=True
)

# SocialLinkFormSet = modelformset_factory(
#     SocialLink,
#     fields=['icon', 'name', 'url'],
#     extra=1,
#     can_delete=True,
# )
