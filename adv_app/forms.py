from django import forms
from django.forms import inlineformset_factory, Textarea
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm

from .models import Adv, User, Reply
from ckeditor_uploader.widgets import CKEditorUploadingWidget


import datetime

class AdvForm(forms.ModelForm):
    head_adv = forms.CharField(required=False)
    text_adv = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Adv
        fields = ['head_adv', 'text_adv', 'category_name', 'content']

    def clean(self):
        cleaned_data = super().clean()
        head_adv = cleaned_data.get("head_adv")
        text_adv = cleaned_data.get("text_adv")
        if text_adv is not None and len(text_adv) < 20:
            raise ValidationError({
                "text_adv": "Текст не может быть менее 20 символов."
            })
        if not head_adv:
            cleaned_data['head_adv'] = datetime.datetime.now()

        return cleaned_data

class CreateReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text_reply']
        labels = {'text_reply':'Ваш комментарий:'}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text_reply'].widget = Textarea(attrs={'rows': 5, 'value' : 'Оставьте комментарий'})

