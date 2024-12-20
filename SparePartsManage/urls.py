"""
URL configuration for SparePartsManage project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    # path("admin/", admin.site.urls),
    # Department Part
    path("depart/list/", views.depart_list),
    path("depart/add/", views.depart_add),
    path("depart/delete/", views.depart_delete),
    path("depart/<int:nid>/edit/", views.depart_edit),

    # User Part
    path("user/list/", views.user_list),
    path("user/add/", views.user_add),
    path("user/<int:nid>/delete/", views.user_delete),
    path("user/<int:nid>/edit/", views.user_edit),

    # Spareparts Part
    path("spareparts/list/", views.spareparts_list),
    path("spareparts/add/", views.spareparts_add),
    path("spareparts/<int:nid>/delete/", views.spareparts_delete),
    path("spareparts/<int:nid>/edit/", views.spareparts_edit),

    path("login/", views.login),
    path("logout/", views.logout),

    path("sale/", views.sale),
    path("purchase/", views.purchase),

    path("data/analyse", views.data_analyse),
    path("api/data", views.api_data),

]
