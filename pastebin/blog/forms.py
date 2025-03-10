from datetime import timedelta

from django import forms
from .models import Paste


class PasteForm(forms.ModelForm):
    time_live = forms.ChoiceField(choices=[], required=False)
    need_password = forms.BooleanField(required=False)
    content = forms.CharField(widget=forms.Textarea(), required=False)

    tags = forms.CharField(
        widget=forms.HiddenInput(attrs={
            'placeholder': 'Выберите подходящие теги ниже...',
            'class': 'post-settings-input',
        }),
        required=False
    )
    syntax = forms.ChoiceField(
        choices=Paste.SYNTAX_CHOICES,
        widget=forms.Select(attrs={'class': 'post-settings-select'}),
        required=True
    )

    class Meta:
        model = Paste
        fields = [
            'syntax', 'title', 'content', 'category',
            'tags', 'access_status', 'time_live',
            'password', 'is_delete_after_read'
        ]
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Введите текст поста...',
                'class': 'post-editor1',
                'rows': 10,
                'data-editor': 'codemirror',
                'required': False
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'Введите название...',
                'class': 'post-settings-input'
            }),
            'access_status': forms.Select(attrs={
                'class': 'post-settings-select'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Пароль',
                'class': 'post-settings-input'
            }),
            'is_delete_after_read': forms.CheckboxInput(attrs={
                'class': 'post-settings-checkbox'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['time_live'].choices = [
            (0, 'Никогда'),
            (timedelta(minutes=2).total_seconds(), 'Через 2 минуты'),
            (timedelta(hours=1).total_seconds(), 'Через 1 час'),
            (timedelta(days=1).total_seconds(), 'Через 1 день'),
            (timedelta(weeks=1).total_seconds(), 'Через 1 неделю'),
        ]
