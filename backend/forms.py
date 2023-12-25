from django import forms


class AddItemForm(forms.Form):
    order_id = forms.IntegerField(label="Номер вашей корзины")
    quantity = forms.IntegerField(label="Количество товара", initial=1)
