from django import forms

from .models import Post, Comment


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



class PostAdminForm(forms.ModelForm):
    md_file = forms.FileField(
        required=False,
        label='آپلود فایل مارک‌داون (.md)',
        help_text='اگه انتخاب کنی، جایگزین متن پایین می‌شه.',
    )

    class Meta:
        model = Post
        fields = '__all__'

    def clean(self):
        cleaned = super().clean()
        md_file = cleaned.get('md_file')
        if md_file:
            cleaned['content'] = md_file.read().decode('utf-8')
        return cleaned