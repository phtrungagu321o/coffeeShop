from django.conf import settings
from django.db import models
from django.utils.crypto import get_random_string
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from store.models import Product


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="order_user")
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, blank=True)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=3)
    order_key = models.CharField(max_length=20, default=get_random_string)
    payment_option = models.CharField(max_length=200, blank=True)
    billing_status = models.BooleanField(default=False)
    Problem = models.TextField(blank=True)
    rating = models.IntegerField(default=100, blank=True)
    isRate = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_items',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ("order",)


class save_List(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="save_user")
    title = models.CharField(max_length=50, default="None", blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)


class save_Item_List(models.Model):
    save_list = models.ForeignKey(save_List,
                                  related_name='items_save_list',
                                  on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='save_item',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ("save_list",)


class Order_Direct(models.Model):
    phone = PhoneNumberField(_('Số điện thoại'), max_length=50, error_messages={
        'required': 'Xin lỗi, đây không phải là số điện thoại'
    })
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_paid = models.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return str(self.created)


class Order_Item_Direct(models.Model):
    order_direct = models.ForeignKey(Order_Direct,
                                     related_name='order_direct_id',
                                     on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='order_direct_item',
                                on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=3)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ("order_direct",)
