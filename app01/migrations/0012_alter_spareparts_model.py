# Generated by Django 4.2.6 on 2024-12-08 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app01", "0011_alter_editlog_new_info"),
    ]

    operations = [
        migrations.AlterField(
            model_name="spareparts",
            name="model",
            field=models.CharField(max_length=512, verbose_name="Model"),
        ),
    ]
