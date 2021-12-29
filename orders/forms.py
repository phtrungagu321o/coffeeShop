from django import forms

from .models import Order_Direct


class Order_Direct_Form(forms.ModelForm):
    class Meta:
        model = Order_Direct
        fields = ["phone", ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].widget.attrs.update(
            {"class": "phone-not-user", "placeholder": "Nhập (+84 <số điện thoại của bạn>)", "value": "+84 "})
