import os

import stripe
from django.db.models import F, Sum
from django.shortcuts import redirect, render
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.forms import AddItemForm
from backend.models import Coupon, Item, Order, OrderItem

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")


# функция для работы с библиотекой stripe
@api_view(["GET"])
def get_stripe_session(request, id, *args, **kwargs):
    discounts = None
    coupon = Coupon.objects.filter(order=id)
    order = (
        Order.objects.filter(id=id)
        .annotate(
            total_sum=Sum(
                F("ordered_items__quantity") * F("ordered_items__item__price")
            )
        )
        .distinct()[0]
    )
    if coupon:
        stripe_coupon = stripe.Coupon.create(
            percent_off=coupon[0].discount,
            duration="once",
        )
        discounts = [{"coupon": stripe_coupon.id}]
        Coupon.objects.filter(order=id).delete()
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price_data": {
                        "unit_amount": order.total_sum * 100,
                        "product_data": {"name": f"Заказ номер {order.id}"},
                        "currency": order.currency,
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
            discounts=discounts,
            success_url=os.getenv("YOUR_DOMAIN") + "/success/",
            cancel_url=os.getenv("YOUR_DOMAIN") + "/cancel/",
            currency=order.currency,
        )
    except Exception as error:
        return Response({"Status": False, "Errors": str(error)})
    return redirect(checkout_session.url)


# функция для работы c корзиной
@api_view(["GET"])
def get_order_buy(request, id, *args, **kwargs):
    discount = None
    coupon = Coupon.objects.filter(order=id)
    order = (
        Order.objects.filter(id=id)
        .annotate(
            total_sum=Sum(
                F("ordered_items__quantity") * F("ordered_items__item__price")
            )
        )
        .distinct()
    )
    items = OrderItem.objects.filter(order=id)
    if not order:
        return render(request, "order.html", {"items": None})
    if coupon:
        discount = coupon[0].discount
    return render(
        request,
        "order.html",
        {"order": order[0], "items": items, "discount": discount},
    )


# функция для работы cо списком товаров
@api_view(["GET"])
def get_items(request, *args, **kwargs):
    items = Item.objects.all()
    if not items:
        return render(request, "items.html", {"items": None})
    count = len(items)
    form = AddItemForm()
    return render(
        request,
        "items.html",
        {"form": form, "count": count, "items": items},
    )


# функция для добавления товаров в корзину
@api_view(["GET"])
def add_item(request, id, *args, **kwargs):
    order_id = request.GET.get("order_id")
    quantity = request.GET.get("quantity")
    order = Order.objects.filter(id=order_id)
    item = Item.objects.filter(id=id)
    if not order:
        return render(
            request, "add_delete_item.html", {"title": "Ошибка", "order_id": None}
        )
    try:
        OrderItem.objects.create(order=order[0], item=item[0], quantity=quantity)
    except Exception as error:
        return Response({"Status": False, "Errors": str(error)})
    return render(
        request,
        "add_delete_item.html",
        {"title": "Добавлено", "order_id": order_id, "add": True},
    )


# функция для удаления товаров из корзины
@api_view(["GET"])
def delete_item(request, order_id, item_id, *args, **kwargs):
    try:
        OrderItem.objects.filter(id=item_id).delete()
    except Exception as error:
        return Response({"Status": False, "Errors": str(error)})
    return render(
        request,
        "add_delete_item.html",
        {"title": "Удалено", "order_id": order_id, "add": False},
    )


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")
