"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from backend.views import (add_item, cancel, delete_item, get_items,
                           get_order_buy, get_stripe_session, success)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("buy/<int:id>/", get_stripe_session, name="stripe_id"),
    path("order/<int:id>/", get_order_buy, name="order"),
    path("items/all/", get_items, name="items"),
    path("order/add/<int:id>/", add_item, name="add_item"),
    path("order/delete/<int:order_id>/<int:item_id>/", delete_item, name="delete_item"),
    path("success/", success, name="success"),
    path("cancel/", cancel, name="cancel"),
]
