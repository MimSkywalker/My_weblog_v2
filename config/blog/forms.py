from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    """

    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput())

    class Meta:
        model = Comment
        fields = ["full_name", "email", "subject", "content"]
        widgets = {
            "full_name": forms.TextInput(
                attrs={
                    "class": "vx-input",
                    "placeholder": "نام و نام خانوادگی",
                    "autocomplete": "name",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "vx-input",
                    "placeholder": "ایمیل",
                    "autocomplete": "email",
                }
            ),
            "subject": forms.TextInput(
                attrs={
                    "class": "vx-input",
                    "placeholder": "موضوع دیدگاه",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "vx-input",
                    "placeholder": "دیدگاه خود را بنویسید...",
                    "rows": 5,
                }
            ),
        }
        labels = {
            "full_name": "نام",
            "email": "ایمیل",
            "subject": "موضوع",
            "content": "متن دیدگاه",
        }
