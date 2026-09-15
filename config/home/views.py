from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
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
        context['recaptcha_site_key'] = settings.RECAPTCHA_PUBLIC_KEY
        return context

    def is_ajax(self):
        return self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

    def form_valid(self, form):
        response = super().form_valid(form)  # اینجا رکورد ذخیره میشه
        if self.is_ajax():
            return JsonResponse({
                'success': True,
                'message': 'پیام شما با موفقیت ارسال شد.',
            })
        return response

    def form_invalid(self, form):
        if self.is_ajax():
            errors = {field: list(errs) for field, errs in form.errors.items()}
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        return super().form_invalid(form)


class IndexView(TemplateView):
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['profile'] = Profile.objects.first()


        return context
