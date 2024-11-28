# Generated by Django 4.2.6 on 2024-11-26 22:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Department",
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
                ("title", models.CharField(max_length=32, verbose_name="Title")),
            ],
        ),
        migrations.CreateModel(
            name="SpareParts",
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
                    "series",
                    models.SmallIntegerField(
                        choices=[(1, "Accessory"), (2, "Other")],
                        default=1,
                        verbose_name="Series",
                    ),
                ),
                ("part_no", models.CharField(max_length=32, verbose_name="Part No.")),
                ("model", models.CharField(max_length=64, verbose_name="Model")),
                ("quantity", models.IntegerField(default=0, verbose_name="Quantity")),
            ],
        ),
        migrations.CreateModel(
            name="UserInfo",
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
                ("name", models.CharField(max_length=32, verbose_name="Name")),
                ("password", models.CharField(max_length=64, verbose_name="Password")),
                (
                    "create_time",
                    models.FloatField(default=0, verbose_name="Create Time"),
                ),
                (
                    "gender",
                    models.SmallIntegerField(
                        choices=[(1, "Male"), (2, "Female")],
                        default=1,
                        verbose_name="Gender",
                    ),
                ),
                (
                    "depart_id",
                    models.ForeignKey(
                        default=999,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.department",
                        verbose_name="Department",
                    ),
                ),
            ],
        ),
    ]
