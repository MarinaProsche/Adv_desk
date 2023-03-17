from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError

from .models import Adv, Author, User, Media
import datetime

class AdvForm(forms.ModelForm):
    head_adv = forms.CharField(required=False)

    class Meta:
        model = Adv
        fields = ['head_adv', 'text_adv', 'category_name']

    def __init__(self, author, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.author = author

    def save(self, commit=True):
        self.instance.author = Author.objects.filter(user=self.author).first()
        return super(AdvForm, self).save(commit=commit)

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


class AddMediaForm(forms.ModelForm):

    class Meta:
        model = Media
        fields = ['content']

AddMediaFormSet = inlineformset_factory(
    Adv, Media, form=AddMediaForm,
    extra=1, can_delete=True, can_delete_extra=True
)
