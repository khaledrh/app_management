# Generated by Django 5.1 on 2024-08-17 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0003_alter_app_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='app',
            name='slug',
            field=models.SlugField(default=''),
        ),
    ]
