# Generated by Django 4.2.3 on 2023-08-12 11:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("competition", "0005_competition_time_string"),
    ]

    operations = [
        migrations.AddField(
            model_name="setting",
            name="broad_cast_name",
            field=models.CharField(default="운동회가 망하지 않게 하기위해 무한 전화를 거는 김민준", max_length=100),
        ),
    ]
