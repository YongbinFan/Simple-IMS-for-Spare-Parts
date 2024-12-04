# Generated by Django 4.2.6 on 2024-12-03 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0004_spareparts_last_edit"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userinfo",
            name="depart_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="app01.department",
                verbose_name="Department",
            ),
        ),
        migrations.CreateModel(
            name="Trade",
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
                ("quantity", models.IntegerField(default=0, verbose_name="Quantity")),
                (
                    "other",
                    models.CharField(
                        blank=True, max_length=256, null=True, verbose_name="Other"
                    ),
                ),
                (
                    "trade_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="Trade Time"),
                ),
                (
                    "spareparts_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="app01.spareparts",
                        verbose_name="Spare Part",
                    ),
                ),
            ],
        ),
    ]
