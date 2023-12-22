from django.db import models

CURRENCY_CHOICES = (
    ("usd", "Доллары"),
    ("eur", "Евро"),
)


class Item(models.Model):
    name = models.CharField(max_length=80, verbose_name="Название", blank=False)
    description = models.CharField(max_length=150, verbose_name="Описание", blank=True)
    price = models.PositiveIntegerField(verbose_name="Цена", blank=False)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Список товаров"
        ordering = ("-name",)

    def __str__(self):
        return self.name


class Order(models.Model):
    dt = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(
        verbose_name="Валюта", choices=CURRENCY_CHOICES, max_length=3, default="usd"
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Список заказов"
        ordering = ("-dt",)

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        related_name="ordered_items",
        blank=True,
        on_delete=models.CASCADE,
    )

    item = models.ForeignKey(
        Item,
        verbose_name="Информация о товаре",
        related_name="ordered_items",
        blank=True,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Заказанная позиция"
        verbose_name_plural = "Список заказанных позиций"

    def __str__(self):
        return str(self.id)


class Coupon(models.Model):
    discount = models.PositiveIntegerField(verbose_name="Процент")
    dt = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey(
        Order,
        verbose_name="Заказ",
        related_name="ordered_coupons",
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Купон"
        verbose_name_plural = "Список купонов"

    def __str__(self):
        return str(self.discount)
