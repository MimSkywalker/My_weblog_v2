from django.shortcuts import render
from .models import Contact
from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .forms import ContactForm
from resume.models import Profile, SocialLink
from resume.models import Profile


class ContactView(CreateView):
    model = Contact
    template_name = 'home/contact.html'
    success_url = reverse_lazy('home:contact')
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.first()

        return context


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = Profile.objects.first()


        return context
