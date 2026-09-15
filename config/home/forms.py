from django import forms
from .models import Contact
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV3

class ContactForm(forms.ModelForm):

    captcha = ReCaptchaField(
        widget=ReCaptchaV3(action='contact'),
        label='',
        error_messages={
            'required': 'تأیید هویت ناموفق بود، لطفاً دوباره تلاش کنید.',
        },
    )
    class Meta:
        model = Contact
        fields = ['full_name', 'email', 'subject', 'message']

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        full_name = full_name.strip()
        if len(full_name) <= 2:
            raise forms.ValidationError('نام بسیار کوتاه است.')

        return full_name

    def clean_email(self):
        email = self.cleaned_data['email']
        return email.strip().lower()

    def clean_subject(self):
        subject = self.cleaned_data['subject']
        subject = subject.strip()
        if len(subject) <= 4:
            raise forms.ValidationError('موضوع انتخابی بسیار کوتاه است.')

        return subject
