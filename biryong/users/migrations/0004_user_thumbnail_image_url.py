# Generated by Django 4.2.3 on 2023-07-29 00:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_rename_name_user_nickname"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="thumbnail_image_url",
            field=models.URLField(blank=True, null=True),
        ),
    ]
