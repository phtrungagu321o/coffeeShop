from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecification,
    ProductSpecificationValue,
    ProductType,
    Contact,

)

admin.site.site_header = 'TRUNG HIẾU COFFEE ADMIN'
admin.site.index_title = "Trang quản lí quán cà phê"
admin.site.site_title = 'Cà Phê Trung Hiếu'

class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "fullname", "message")
    list_filter = ("created_at",)


admin.site.register(Contact, ContactAdmin)
admin.site.register(Category, MPTTModelAdmin)


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
    model = ProductSpecificationValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecificationValueInline,
        ProductImageInline,
    ]
