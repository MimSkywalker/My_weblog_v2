from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
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
