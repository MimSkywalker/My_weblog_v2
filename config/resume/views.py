from django.shortcuts import render, redirect
from .models import Profile, Experience, Skill, Education, SocialLink, Expertise
from django.views import View
from . import forms
from .mixins import PortfolioDashboardMixin
from django.views.generic import TemplateView


class PortfolioDashboardView(PortfolioDashboardMixin, View):
    template_name = 'resume/dashboard.html'

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.first()

        context = {
            'profile_form': forms.ProfileForm(instance=profile),
            'experience_formset': forms.ExperienceFormSet(queryset=Experience.objects.all(), prefix='exp'),
            'skill_formset': forms.SkillFormSet(queryset=Skill.objects.all(), prefix='skill'),
            'education_formset': forms.EducationFormSet(queryset=Education.objects.all(), prefix='edu'),
            'expertise_formset': forms.ExpertiseFormSet(queryset=Expertise.objects.all(), prefix='exprt'),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.first()

        profile_form = forms.ProfileForm(
            request.POST, request.FILES, instance=profile)
        experience_formset = forms.ExperienceFormSet(
            request.POST, request.FILES, prefix='exp')
        skill_formset = forms.SkillFormSet(
            request.POST, request.FILES, prefix='skill')
        education_formset = forms.EducationFormSet(
            request.POST, request.FILES, prefix='edu')
        expertise_formset = forms.ExpertiseFormSet(
            request.POST, request.FILES, prefix='exprt')

        profile_valid = profile_form.is_valid()
        exp_valid = experience_formset.is_valid()
        skill_valid = skill_formset.is_valid()
        edu_valid = education_formset.is_valid()
        exprt_valid = expertise_formset.is_valid()
        print("PROFILE:", profile_valid, profile_form.errors)
        print("EXPERIENCE:", exp_valid, experience_formset.errors,
              experience_formset.non_form_errors())
        print("SKILL:", skill_valid, skill_formset.errors,
              skill_formset.non_form_errors())
        print("EDUCATION:", edu_valid, education_formset.errors,
              education_formset.non_form_errors())
        print("EXPERTISE:", exprt_valid, expertise_formset.errors,
              expertise_formset.non_form_errors())

        if all([profile_valid, exp_valid, skill_valid, edu_valid, exprt_valid]):
            profile_form.save()

            experience_formset.save()
            skill_formset.save()
            education_formset.save()
            expertise_formset.save()

            return redirect('resume:resume_manager')

        context = {
            'profile_form': profile_form,
            'experience_formset': experience_formset,
            'skill_formset': skill_formset,
            'education_formset': education_formset,
            'expertise_formset': expertise_formset,
        }
        return render(request, self.template_name, context)


class test(TemplateView):
    template_name = 'resume/resume.html'


class test1(TemplateView):
    template_name = 'home/index.html'


class test2(TemplateView):
    template_name = 'home/contact.html'


class test3(TemplateView):
    template_name = 'blog/blog.html'
