# Generated by Django 4.2.3 on 2023-08-13 03:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("competition", "0011_alter_competition_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="player",
            name="active",
            field=models.BooleanField(default=True, verbose_name="활성화"),
        ),
    ]