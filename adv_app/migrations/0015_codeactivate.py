# Generated by Django 4.1.7 on 2023-03-25 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adv_app', '0014_delete_codeactivate'),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeActivate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=30)),
                ('code', models.CharField(max_length=6)),
            ],
        ),
    ]
