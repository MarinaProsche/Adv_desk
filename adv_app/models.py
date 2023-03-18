from os import path
from django.db import models
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
import adv_project.settings
from ckeditor.fields import RichTextField

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user}'

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
    head_adv = models.CharField(max_length = 50, null=True)
    text_adv = RichTextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category_name = models.CharField(max_length = 20, choices = CATEGORY_NAME, default='other')
    is_active = models.BooleanField(default=True)
                #для того, чтобы если новость удалили, она сохранилась, просто не показывалась

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

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
    #     cache.delete(f'adv-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его

def author_directory_path(instance, filename):
    return path.join(adv_project.settings.MEDIA_ROOT, 'files', str(instance.adv.author_id), filename)

class Media(models.Model):
    adv = models.ForeignKey(Adv, related_name = 'media', on_delete=models.CASCADE)
    content = models.ImageField(upload_to=author_directory_path, null=True)

class Reply(models.Model):
    adv = models.ForeignKey (Adv, on_delete = models.CASCADE)
    user = models.ForeignKey (User, on_delete=models.CASCADE)
    text_reply = models.TextField()
    date_replay = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.text_reply}, {self.date_replay}'
