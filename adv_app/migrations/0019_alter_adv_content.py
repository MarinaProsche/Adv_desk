# Generated by Django 4.1.7 on 2023-03-26 16:44

import adv_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv_app', '0018_adv_content_delete_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adv',
            name='content',
            field=models.ImageField(blank=True, null=True, upload_to=adv_app.models.author_directory_path),
        ),
    ]
