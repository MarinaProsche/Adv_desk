# Generated by Django 4.1.7 on 2023-03-27 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv_app', '0022_alter_adv_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adv',
            name='category_name',
            field=models.CharField(choices=[('tanks', 'Танки'), ('heals', 'Хилы'), ('dd', 'ДД'), ('sailers', 'Торговцы'), ('gildmasters', 'Гилдмастеры'), ('questsgivers', 'Квестгиверы'), ('smith', 'Кузнецы'), ('skinner', 'Кожевники'), ('potionmasters', 'Зельевары'), ('spellmasters', 'Мастера заклинаний'), ('other', 'другое')], default='other', max_length=20, verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='adv',
            name='head_adv',
            field=models.CharField(max_length=50, null=True, verbose_name='Заголовок'),
        ),
    ]
