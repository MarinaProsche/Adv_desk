# Generated by Django 4.1.7 on 2023-03-16 11:18

import adv_app.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv_app', '0003_adv_content_adv_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adv',
            name='image',
            field=models.ImageField(null=True, upload_to=adv_app.models.author_directory_path),
        ),
    ]
