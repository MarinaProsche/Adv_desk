# Generated by Django 4.1.7 on 2023-03-19 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adv_app', '0009_alter_reply_adv_alter_reply_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='user',
            new_name='reply_author',
        ),
    ]
