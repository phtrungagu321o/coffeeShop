from django.contrib import admin

from .models import Order, OrderItem, save_List, save_Item_List, Order_Direct, Order_Item_Direct


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "price", "quantity",)
    list_filter = ("order",)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("created", "order_key", "total_paid", "phone", "full_name", "email", "address1", "address2")
    list_filter = ("billing_status",)


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)


class DirectItemAdmin(admin.ModelAdmin):
    list_display = ("order_direct", "product", "price", "quantity",)
    list_filter = ("order_direct",)


class DirectAdmin(admin.ModelAdmin):
    list_display = ("created", "phone", "total_paid",)
    list_filter = ("created",)


admin.site.register(Order_Direct, DirectAdmin)
admin.site.register(Order_Item_Direct, DirectItemAdmin)
