# Generated by Django 4.2.3 on 2023-08-12 12:14

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("competition", "0009_alter_player_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="player",
            options={"ordering": ["created"]},
        ),
    ]
