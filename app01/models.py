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
    depart_id = models.ForeignKey(verbose_name="Department", to="Department", to_field="id", on_delete=models.SET_NULL,
                                  null=True, blank=True)

    gender_choices = (
        (1, "Male"),
        (2, "Female")
    )
    gender = models.SmallIntegerField(verbose_name="Gender", choices=gender_choices, default=1)

    def __str__(self):
        try:
            dep_str = self.depart_id.title
        except AttributeError:
            dep_str = "/"
        return " ".join([
            "ID:" + str(self.id),
            "Name:" + self.name,
            "Password:" + self.password,
            "Dep:" + dep_str,
            "Gender:" + self.get_gender_display()
        ])


class SpareParts(models.Model):
    series_choices = (
        (1, "Accessory"),
        (2, "Other")
    )
    series = models.SmallIntegerField(verbose_name="Series", choices=series_choices, default=1)
    part_no = models.CharField(verbose_name="Part No.", max_length=32)
    model = models.CharField(verbose_name="Model", max_length=512)
    quantity = models.IntegerField(verbose_name="Quantity", default=0)
    other = models.CharField(verbose_name="Other", max_length=128, blank=True, null=True)
    last_edit = models.DateTimeField(verbose_name="Last Edit Time", auto_now=True)

    def __str__(self):
        try:
            other_str = str(self.other)
        except TypeError:
            other_str = "/"
        return "*".join([
            str(self.id),
            self.get_series_display(),
            self.part_no,
            self.model,
            str(self.quantity),
            other_str
        ])


class Trade(models.Model):
    # if quantity > 0 means purchase new spareparts from vendor, quantity<0 means sell spareparts to customer
    spareparts_id = models.ForeignKey(verbose_name="Spare Part", to="SpareParts", to_field="id",
                                      on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(verbose_name="Quantity", default=0)
    other = models.CharField(verbose_name="Other", default="/", max_length=256)
    trade_time = models.DateTimeField(verbose_name="Trade Time", auto_now_add=True)
    created_by = models.ForeignKey(verbose_name="Created By", to="UserInfo", to_field="id", on_delete=models.SET_NULL,
                                   null=True, blank=True)


class EditLog(models.Model):
    # create old_info could be null
    old_info = models.CharField(verbose_name="Old Info", max_length=512, null=True, blank=True)
    # delete new_info could be null
    new_info = models.CharField(verbose_name="New Info", max_length=512,null=True, blank=True)
    edit_time = models.DateTimeField(verbose_name="Trade Time", auto_now_add=True)
    created_by = models.ForeignKey(verbose_name="Created By", to="UserInfo", to_field="id", on_delete=models.SET_NULL,
                                   null=True, blank=True)
