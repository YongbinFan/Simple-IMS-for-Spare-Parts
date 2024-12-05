# Generated by Django 4.2.6 on 2024-12-05 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0008_alter_trade_spareparts_id_alter_userinfo_depart_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="trade",
            name="created_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="app01.userinfo",
                verbose_name="Created By",
            ),
        ),
        migrations.CreateModel(
            name="UserInfoEdit",
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
                    "old_info",
                    models.CharField(
                        blank=True, max_length=512, null=True, verbose_name="Old Info"
                    ),
                ),
                ("new_info", models.CharField(max_length=512, verbose_name="New Info")),
                (
                    "edit_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="Trade Time"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="update_to_userinfo",
                        to="app01.userinfo",
                        verbose_name="Created By",
                    ),
                ),
                (
                    "userinfo_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="info_to_userinfo",
                        to="app01.userinfo",
                        verbose_name="User Info",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SparepartsEdit",
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
                    "old_info",
                    models.CharField(
                        blank=True, max_length=512, null=True, verbose_name="Old Info"
                    ),
                ),
                ("new_info", models.CharField(max_length=512, verbose_name="New Info")),
                (
                    "edit_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="Trade Time"),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app01.userinfo",
                        verbose_name="Created By",
                    ),
                ),
                (
                    "spareparts_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="app01.spareparts",
                        verbose_name="Spare Part",
                    ),
                ),
            ],
        ),
    ]