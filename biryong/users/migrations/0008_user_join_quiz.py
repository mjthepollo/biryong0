# Generated by Django 4.2.3 on 2023-08-14 23:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0007_user_chat_name_color"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="join_quiz",
            field=models.BooleanField(default=False),
        ),
    ]
