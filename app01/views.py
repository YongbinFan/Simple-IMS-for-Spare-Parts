import json
import re

from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from django import forms
from django.utils.safestring import mark_safe
from app01.utils.pagination import Pagination
from app01.utils.encrypt import md5
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
        # now_timestamp = datetime.datetime.now().timestamp()
        form = UserModelForm(request.POST)
        # form.instance.create_time = now_timestamp
        form.save()

        return redirect("/user/list/")
    else:
        print(form.errors)
        return render(request, "user_add.html", {"form": form})


def user_edit(request, nid):
    """Edit User"""
    row_object = models.UserInfo.objects.filter(id=nid).first()
    row_object.password = "******"
    print(row_object.password)
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
        print("valid")
        form.save()
        return redirect("/user/list/")
    # print(form.errors)
    return render(request, "user_add.html", {"form": form})


def user_delete(request, nid):
    """Delete User"""
    models.UserInfo.objects.filter(id=nid).delete()

    return redirect("/user/list/")


def spareparts_list(request):
    """ Spare Parts List """
    # fake data
    # for i in range(300):
    #     import random
    #     models.SpareParts.objects.create(
    #         series=str(random.randint(1, 2)),
    #         part_no=str(random.randint(10000000, 99999999)),
    #         model=str(random.randint(1000, 9999)),
    #         quantity=random.randint(0, 1000)
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
    try:
        page = int(request.GET.get("page", 1))
    except:
        page = 1
    if page <= 0:
        page = 1

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

        return redirect("/spareparts/list/")
    else:
        return render(request, "user_add.html", {"form": form})


def spareparts_edit(request, nid):
    """Edit Spare Parts"""
    row_object = models.SpareParts.objects.filter(id=nid).first()
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
        return redirect("/spareparts/list/")
    # print(form.errors)
    return render(request, "spareparts_add.html", {"form": form})


def spareparts_delete(request, nid):
    """Delete User"""
    models.SpareParts.objects.filter(id=nid).delete()

    return redirect("/spareparts/list/")


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
def purchase(request):
    if request.method == "GET":
        queryset = models.SpareParts.objects.all()
        info = {
            "queryset": queryset
        }
        return render(request, "purchase.html", info)

    data = json.loads(request.body)
    for item in data:
        obj_str = item.get("obj")
        match = re.search(r"ID:(\d+)", obj_str)
        if match:
            item_id = int(match.group(1))
            item_quantity = int(item.get("quantity"), 0)
            print(item_id, item_quantity)
    # print(type(data[0]))
    # print(data)
    # print(data[0]["obj"])
    return HttpResponse("Successful sent data!")
