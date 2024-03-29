# Generated by Django 4.2.4 on 2023-09-11 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend_app", "0008_alter_image_index"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.CharField(max_length=100)),
                ("points", models.IntegerField()),
                ("isCheck", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
