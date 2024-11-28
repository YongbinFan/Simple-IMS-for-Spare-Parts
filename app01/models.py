from django.db import models
import datetime


# Create your models here.
class Department(models.Model):
    """ Department table """
    title = models.CharField(verbose_name="Title", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    name = models.CharField(verbose_name="Name", max_length=32)
    password = models.CharField(verbose_name="Password", max_length=64)
    create_time = models.DateTimeField(verbose_name="Create Time", auto_now_add=True)
    depart_id = models.ForeignKey(verbose_name="Department", to="Department", to_field="id", on_delete=models.CASCADE,
                                  default=999)

    gender_choices = (
        (1, "Male"),
        (2, "Female")
    )
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choices, default=1)


class SpareParts(models.Model):
    series_choices = (
        (1, "Accessory"),
        (2, "Other")
    )
    series = models.SmallIntegerField(verbose_name="Series", choices=series_choices, default=1)
    part_no = models.CharField(verbose_name="Part No.", max_length=32)
    model = models.CharField(verbose_name="Model", max_length=64)
    quantity = models.IntegerField(verbose_name="Quantity", default=0)
    other = models.CharField(verbose_name="Other", max_length=128,blank=True, null=True)
    last_edit = models.DateTimeField(verbose_name="Last Edit Time", auto_now=True)

