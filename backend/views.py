import os

import stripe
from django.db.models import F, Sum
from django.shortcuts import redirect, render
from dotenv import load_dotenv
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.models import Coupon, Order, OrderItem

load_dotenv()

stripe.api_key = os.getenv("STRIPE_API_KEY")


class StripeSession(APIView):
    """
    Класс для работы с библиотекой stripe
    """

    def get(self, request, id, *args, **kwargs):
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


class OrderBuy(APIView):
    """
    Класс для работы c покупками
    """

    def get(self, request, id, *args, **kwargs):
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
            return render(request, "checkout.html", {"items": None})
        if coupon:
            discount = coupon[0].discount
        return render(
            request,
            "checkout.html",
            {"order": order[0], "items": items, "discount": discount},
        )


def success(request):
    return render(request, "success.html")


def cancel(request):
    return render(request, "cancel.html")
