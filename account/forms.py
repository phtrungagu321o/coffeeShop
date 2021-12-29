from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm,
                                       SetPasswordForm)

from .models import Customer, Address


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line", "address_line2", "town_city", "postcode", ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["full_name"].widget.attrs.update(
            {"class": "log__form-input", "placeholder": "Nhập tên đầy đủ của bạn"}
        )
        self.fields["phone"].widget.attrs.update(
            {"class": "log__form-input", "placeholder": "Nhập (+84 <số điện thoại của bạn>)", "value": "+84 "})
        self.fields["address_line"].widget.attrs.update(
            {"class": "log__form-input", "placeholder": "Nhập địa chỉ đầu tiên của bạn"}
        )
        self.fields["address_line2"].widget.attrs.update(
            {"class": "log__form-input", "placeholder": "Nhập địa chỉ thứ 2 của bạn (không bắt buộc)"}
        )
        self.fields["town_city"].widget.attrs.update(
            {"class": "log__form-input", "placeholder": "Tên thành phố"}
        )
        self.fields["postcode"].widget.attrs.update(
            {"class": "log__form-input", "placeholder": "Nhập mã bưu điện của bạn (không bắt buộc)"}
        )


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'log__form-input', 'placeholder': 'Nhập Email của bạn', 'id': 'login-username'}))
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput(
        attrs={
            'class': 'log__form-input',
            'placeholder': 'Nhập mật khẩu của bạn',
            'id': 'login-pwd',
        }
    ))


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Tên tài khoản', min_length=4, max_length=50, help_text='Bắt buộc')
    email = forms.EmailField(max_length=100, help_text='Bắt buộc', error_messages={
        'required': 'Xin lỗi, bạn cần một email'
    })

    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Nhập lại mật khẩu', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        if Customer.objects.filter(name=user_name).exists():
            raise forms.ValidationError('Tên đăng kí đã được sử dụng')
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Hai trường mật khẩu không khớp')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        print(Customer.objects.filter(email=email).count())
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError(
                'Vui lòng sử dụng Email khác, email đã được sử dụng')
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update(
            {'class': 'log__form-input', 'placeholder': 'Nhập tên cá nhân'})
        self.fields['email'].widget.attrs.update(
            {'class': 'log__form-input', 'placeholder': 'Nhập địa chỉ Email', 'name': 'email', 'id': 'id_email'})
        self.fields['password'].widget.attrs.update(
            {'class': 'log__form-input', 'placeholder': 'Nhập mật khẩu'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'log__form-input', 'placeholder': 'Nhập lại mật khẩu'})


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(
        label='Tài khoản email', max_length=200, widget=forms.TextInput(
            attrs={'class': 'log__form-input', 'placeholder': 'email', 'id': 'form-email', 'readonly': 'readonly'}))

    name = forms.CharField(
        label='Tên cá nhân', min_length=4, max_length=50, widget=forms.TextInput(
            attrs={'class': 'log__form-input', 'placeholder': 'First-name', 'id': 'form-firstname'}))

    class Meta:
        model = Customer
        fields = ('email', 'name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(
        attrs={'class': 'log__form-input', 'placeholder': 'Email', 'id': 'form-email'}
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Rất tiếc, chúng tôi không thể tìm thấy địa chỉ email đó'
            )
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(
        label='Mật khẩu mới', widget=forms.PasswordInput(
            attrs={'class': 'confirm__input', 'placeholder': 'Mật khẩu mới', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(
        label='Nhập lại mật khẩu mới', widget=forms.PasswordInput(
            attrs={'class': 'confirm__input', 'placeholder': 'Mật khẩu mới', 'id': 'form-newpass2'}))
