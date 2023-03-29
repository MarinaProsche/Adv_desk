import os
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
import adv_project.settings
from ckeditor.fields import RichTextField


class CodeActivate(models.Model):
    user = models.CharField(max_length=30)
    code = models.CharField(max_length=6)

def author_directory_path(instance, filename):
    return os.path.join(f'user_{instance.author.id}', filename)

CATEGORY_NAME = [('tanks', 'Танки'),
                 ('heals', 'Хилы'),
                 ('dd', 'ДД'),
                 ('sailers', 'Торговцы'),
                 ('gildmasters', 'Гилдмастеры'),
                 ('questsgivers', 'Квестгиверы'),
                 ('smith', 'Кузнецы'),
                 ('skinner', 'Кожевники'),
                 ('potionmasters', 'Зельевары'),
                 ('spellmasters', 'Мастера заклинаний'),
                 ('other', 'другое')]


class Adv(models.Model):
    date_adv = models.DateTimeField(auto_now_add=True)
    head_adv = models.CharField(max_length = 50, null=True, verbose_name = 'Заголовок')
    text_adv = RichTextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "authoruser")
    category_name = models.CharField(max_length = 20, choices = CATEGORY_NAME, default='other', verbose_name = 'Категория')
    is_active = models.BooleanField(default=True)
                #для того, чтобы если новость удалили, она сохранилась, просто не показывалась
    content = models.ImageField(upload_to=author_directory_path, null=True, blank = True)

    def preview(self):
        if len(self.text_adv) < 128:
            return self.text_adv
        else:
            text_adv_short = self.text_adv[0:129]
            return f'{text_adv_short}...'

    def __str__(self):
        return f'{self.head_adv}, {self.category_name}, {self.date_adv}, {self.text_adv[0:20]}'

    def get_absolute_url(self):
        return reverse('nadv', args=[str(self.id)])

    @property
    def adv_popular(self):
        self.rating = 0
        all_reply = Reply.objects.filter(adv=self, status=True).count()
        return all_reply > 3
#     популярные объявления с комментариями больше трех (для периодических задач)

class Reply(models.Model):
    adv = models.ForeignKey(Adv, on_delete = models.CASCADE, related_name='reply')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reply')
    text_reply = models.TextField()
    date_replay = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(verbose_name='Видимость', default=False)

    def __str__(self):
        return f'{self.author}, {self.text_reply}, {self.date_replay}'

    def accept_reply(self):
        self.status = True
        self.save()