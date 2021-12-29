import django_filters
from django_filters import CharFilter

from .models import *


class ProductFilter(django_filters.FilterSet):
    slug = CharFilter(field_name='slug', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ["product_type", "title", ]

