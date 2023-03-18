from django.contrib import admin
from .models import User, Adv, Reply, Author, Media
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdvAdminForm(forms.ModelForm):
    text_adv = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Adv
        fields = '__all__'


class AdvAdmin(admin.ModelAdmin):
    form = AdvAdminForm


admin.site.register(Adv)
admin.site.register(Reply)
admin.site.register(Author)
admin.site.register(Media)

# Register your models here.
