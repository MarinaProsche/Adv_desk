# Generated by Django 4.1.7 on 2023-03-29 12:50

import adv_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv_app', '0024_delete_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adv',
            name='content',
            field=models.ImageField(blank=True, null=True, upload_to=adv_app.models.author_directory_path),
        ),
    ]
