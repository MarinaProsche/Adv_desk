# Generated by Django 4.1.7 on 2023-03-14 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adv_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Post',
            new_name='Adv',
        ),
        migrations.RenameField(
            model_name='adv',
            old_name='date_post',
            new_name='date_adv',
        ),
        migrations.RenameField(
            model_name='adv',
            old_name='head_post',
            new_name='head_adv',
        ),
        migrations.RenameField(
            model_name='adv',
            old_name='text_post',
            new_name='text_adv',
        ),
        migrations.RenameField(
            model_name='reply',
            old_name='post',
            new_name='adv',
        ),
    ]
