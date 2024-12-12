import json
import re

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from app01 import models
from django import forms
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.encrypt import md5
from app01.utils.trade import Trade
from app01.utils.data_analyse import inventory_distribution, SaleData
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def depart_list(request):
    """ Department List """
    queryset = models.Department.objects.all()
    info = {
        'queryset': queryset
    }

    return render(request, "depart_list.html", info)


def depart_add(request):
    """Add New Department"""
    if request.method == "GET":
        return render(request, "depart_add.html")
    title = request.POST.get("title")
    models.Department.objects.create(title=title)

    return redirect("/depart/list/")


def depart_delete(request):
    """Delete Department"""
    nid = request.GET.get("nid")
    models.Department.objects.filter(id=nid).delete()

    return redirect("/depart/list/")


def depart_edit(request, nid):
    """Edit Department"""
    row_object = models.Department.objects.filter(id=nid).first()
    if request.method == "GET":
        info = {
            "row_object": row_object
        }
        return render(request, "depart_edit.html", info)

    title = request.POST.get("title")

    models.Department.objects.filter(id=nid).update(title=title)
    return redirect("/depart/list/")


def user_list(request):
    """ User List """
    queryset = models.UserInfo.objects.all()
    info = {
        'queryset': queryset
    }
    return render(request, "user_list.html", info)


class UserModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ["name", "password", "depart_id", "gender"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    # encrypt password
    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        pwd = md5(pwd)
        return pwd


def user_add(request):
    """Add New User"""
    form = UserModelForm()
    if request.method == "GET":
        return render(request, "user_add.html", {"form": form})
    form = UserModelForm(data=request.POST)

    if form.is_valid():
        form = UserModelForm(request.POST)
        form.save()
        new_obj = models.UserInfo.objects.last()
        log_info = {
            "new_info": str(new_obj),
            "created_by_id": request.session["info"]["id"]
        }
        models.EditLog.objects.create(**log_info)

        return redirect("/user/list/")
    else:
        return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    """Edit User"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    old_info = str(row_object)
    row_object.password = "******"
    form = UserModelForm(instance=row_object)
    form.fields["password"].initial = "******"

    if request.method == "GET":
        info = {
            "row_object": row_object,
            "form": form
        }
        return render(request, "user_edit.html", info)

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        post_data = request.POST.copy()
        if post_data["depart_id"] != "":
            depart_id = post_data["depart_id"]
        else:
            depart_id = None

        # Check if the password field should be removed
        if post_data.get('password') == '******':

            models.UserInfo.objects.filter(id=row_object.id).update(
                name=post_data["name"],
                depart_id=depart_id,
                gender=int(post_data["gender"])
            )
        else:
            # Pass the modified data to the form
            form.save()
        new_info = str(models.UserInfo.objects.filter(id=row_object.id).first())
        log_info = {
            "old_info": old_info,
            "new_info": new_info,
            "created_by_id": request.session["info"]["id"]
        }
        models.EditLog.objects.create(**log_info)

        return redirect("/user/list/")
    return render(request, "user_edit.html", {"form": form})


def user_delete(request, nid):
    """Delete User"""
    obj = models.UserInfo.objects.filter(id=nid).first()
    log_info = {
        "old_info": str(obj),
        # "new_info": new_info,
        "created_by_id": request.session["info"]["id"]
    }
    models.EditLog.objects.create(**log_info)
    models.UserInfo.objects.filter(id=nid).delete()

    return redirect("/user/list/")


def spareparts_list(request, faker=None):
    """ Spare Parts List """
    # fake data

    # import csv
    # import random
    # from faker import Faker
    # csv_file = "products.csv"  # Replace with the path to your CSV file
    # with open(csv_file, newline='', encoding='utf-8') as file:
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         models.SpareParts.objects.create(
    #             part_no=row["part_no"],
    #             model=row["model"][7:],
    #             quantity=random.randint(0, 500),  # Generate random quantity
    #             series=random.choice(["1", "2"])  # Random series
    #         )
    #
    # trade fake data
    # faker = Faker()
    # for _ in range(300):
    #     quantity = random.randint(-50, 50)  # Random quantity
    #     other = "/"  # Static value
    #     trade_time = faker.date_time_between(start_date="-2y", end_date="now")  # Random date within the last year
    #     spareparts_id_id = random.randint(5, 73)  # Assuming foreign keys range from 1 to 20
    #     created_by_id = random.randint(1, 2)  # Assuming foreign keys range from 1 to 5
    #     models.Trade.objects.create(
    #         spareparts_id_id=spareparts_id_id,
    #         created_by_id=created_by_id,
    #         trade_time=trade_time,
    #         other=other,
    #         quantity=quantity
    #     )

    data_dict = {}

    series = request.GET.get("series", "")
    if series:
        data_dict["series"] = int(series)

    part_no = request.GET.get("part_no__contains", "")
    if part_no:
        data_dict["part_no__contains"] = part_no

    model = request.GET.get("model__contains", "")
    if model:
        data_dict["model__contains"] = model

    quantity_gte = request.GET.get("quantity__gte", "")
    if quantity_gte:
        try:
            quantity_gte = int(quantity_gte)
            data_dict["quantity__gte"] = quantity_gte
        except:
            pass

    quantity_lte = request.GET.get("quantity__lte", "")
    if quantity_lte:
        try:
            quantity_lte = int(quantity_lte)
            data_dict["quantity__lte"] = quantity_lte
        except:
            pass

    page_object = Pagination(request, data_dict=data_dict)
    queryset = page_object.queryset
    page_str = page_object.page_str

    info = {
        'queryset': queryset,
        "search_value": data_dict,
        "page_str": mark_safe(page_str),
    }

    return render(request, "spareparts_list.html", info)


class SparepartsModelForm(forms.ModelForm):
    class Meta:
        model = models.SpareParts
        # fields = "__all__"
        # exclude = ["name"]
        fields = ["series", "part_no", "model", "quantity", "other"]
        # widgets = {
        #     "name": forms.TextInput(attrs={"class": "form-control"}),
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {"class": "form-control"}

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 0:
            raise forms.ValidationError("Quantity need to be positive.")
        return quantity


def spareparts_add(request):
    """Add New Spareparts"""
    form = SparepartsModelForm()
    if request.method == "GET":
        return render(request, "spareparts_add.html", {"form": form})
    form = SparepartsModelForm(data=request.POST)

    if form.is_valid():
        form.save()
        # add info to EditLog
        new_obj = models.SpareParts.objects.last()
        log_info = {
            "new_info": str(new_obj),
            "created_by_id": request.session["info"]["id"]
        }
        models.EditLog.objects.create(**log_info)

        return redirect("/spareparts/list/")
    else:
        return render(request, "user_add.html", {"form": form})


def spareparts_edit(request, nid):
    """Edit Spare Parts"""
    row_object = models.SpareParts.objects.filter(id=nid).first()
    old_info = str(row_object)
    form = SparepartsModelForm(instance=row_object)
    if request.method == "GET":
        info = {
            "row_object": row_object,
            "form": form
        }
        return render(request, "spareparts_edit.html", info)

    form = SparepartsModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        new_info = str(models.SpareParts.objects.filter(id=row_object.id).first())
        log_info = {
            "old_info": old_info,
            "new_info": new_info,
            "created_by_id": request.session["info"]["id"]
        }
        models.EditLog.objects.create(**log_info)
        return redirect("/spareparts/list/")
    return render(request, "spareparts_add.html", {"form": form})


def spareparts_delete(request, nid):
    """Delete User"""
    exists = models.SpareParts.objects.filter(id=nid).exists()
    if not exists:
        return JsonResponse({"status": False})

    obj = models.SpareParts.objects.filter(id=nid).first()
    log_info = {
        "old_info": str(obj),
        # "new_info": new_info,
        "created_by_id": request.session["info"]["id"]
    }
    models.EditLog.objects.create(**log_info)
    models.SpareParts.objects.filter(id=nid).delete()

    return JsonResponse({"status": True})


class LoginForm(forms.Form):
    name = forms.CharField(
        label="User Name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        required=True
    )

    def clean_password(self):
        password = md5(self.cleaned_data.get("password"))
        return password


def login(request):
    if request.method == "GET":
        form = LoginForm()
        info = {
            "form": form
        }
        return render(request, "login.html", info)
    form = LoginForm(data=request.POST)
    info = {
        "form": form
    }
    if form.is_valid():
        user_object = models.UserInfo.objects.filter(**form.cleaned_data).filter().first()
        # cannot find the user with the name and pwd
        if not user_object:
            form.add_error("name", "User name or password is wrong!")
            form.add_error("password", "User name or password is wrong!")
            return render(request, "login.html", info)
        # validate pass
        request.session["info"] = {
            "id": user_object.id,
            "name": user_object.name
        }
        return redirect("/spareparts/list/")
    return render(request, "login.html", info)


def logout(request):
    request.session.clear()
    return redirect("/login/")


@csrf_exempt
def sale(request):
    if request.method == "GET":
        queryset = models.SpareParts.objects.all()
        info = {
            "queryset": queryset,
            "trade_way": "Sale"
        }
        return render(request, "trade.html", info)

    trade_obj = Trade(request, trade_way="sale")
    response = trade_obj.get_response()

    return JsonResponse(response)


@csrf_exempt
def purchase(request):
    if request.method == "GET":
        queryset = models.SpareParts.objects.all()
        info = {
            "queryset": queryset,
            "trade_way": "Purchase"
        }
        return render(request, "trade.html", info)

    trade_obj = Trade(request, trade_way="purchase")
    response = trade_obj.get_response()

    return JsonResponse(response)


def data_analyse(request):
    return render(request, "data_analyse.html")


def api_data(request):
    sale_data = SaleData()
    info = {
        "inventory_distribution": inventory_distribution(),
        "top_sale_list": sale_data.get_sale_data(15),
        "sale_vs_inventory": sale_data.get_sale_vs_inventory(30),
        "asc_current_inventory": sale_data.get_current_inventory(15, sort="asc"),
        "desc_current_inventory": sale_data.get_current_inventory(15, sort="desc"),
    }

    print(sale_data.get_current_inventory(15, sort="asc"))
    return JsonResponse(info)
