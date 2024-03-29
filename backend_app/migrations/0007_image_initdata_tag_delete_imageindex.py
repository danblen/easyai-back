# Generated by Django 4.2.4 on 2023-09-10 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("backend_app", "0006_imageindex"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
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
                (
                    "image",
                    models.ImageField(
                        blank=True, default=None, null=True, upload_to="user_images/"
                    ),
                ),
                ("tag", models.CharField(max_length=100)),
                ("status", models.CharField(blank=True, max_length=255, null=True)),
                ("index", models.IntegerField()),
                ("time", models.DateTimeField(auto_now_add=True)),
                ("views", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="InitData",
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
                ("image_urls", models.TextField(blank=True)),
                ("app_version", models.CharField(blank=True, max_length=20)),
                ("app_name", models.CharField(blank=True, max_length=100)),
                ("app_description", models.TextField(blank=True)),
                ("other_config", models.JSONField(blank=True, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Tag",
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
                ("name", models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.DeleteModel(
            name="ImageIndex",
        ),
    ]
