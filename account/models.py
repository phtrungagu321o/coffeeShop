import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):
    def validateEmail(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_('Bạn phải cung cấp một địa chỉ email hợp lệ'))

    def create_superuser(self, email, name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser phải được gán cho is_staff = True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser phải được gán cho is_superuser = True')

        if email:
            email = self.normalize_email(email)
            self.validateEmail(email)
        else:
            raise ValueError(_('Tài khoản superUser: bạn phải cung cấp một địa chỉ email hợp lệ'))

        return self.create_user(email, name, password, **other_fields)

    def create_user(self, email, name, password, **other_fields):
        if email:
            email = self.normalize_email(email)
            self.validateEmail(email)
        else:
            raise ValueError(_('Tài khoản: bạn phải cung cấp một địa chỉ email hợp lệ'))

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **other_fields)

        user.set_password(password)
        user.save()
        return user


class Customer(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email address'), unique=True)
    name = models.CharField(max_length=150)
    mobile = PhoneNumberField(blank=True, help_text='Số điện thoại liên hệ')
    # User Status
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = "Accounts"
        verbose_name_plural = "Accounts"

    def email_user(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.name


class Address(models.Model):
    """
   Address
   """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, verbose_name=_('Customer'), on_delete=models.CASCADE)
    full_name = models.CharField(_('Tên đầy đủ'), max_length=150)
    phone = PhoneNumberField(_('Số điện thoại'), max_length=50, error_messages={
        'required': 'Xin lỗi, đây không phải là số điện thoại'
    })
    postcode = models.CharField(_('Mã bưu điện'), max_length=50, blank=True)
    address_line = models.CharField(_('Địa chỉ 1'), max_length=255)
    address_line2 = models.CharField(_('Địa chỉ 2'), max_length=255, blank=True)
    town_city = models.CharField(_('Thành phố'), max_length=150)
    delivery_instructions = models.CharField(_('Hướng dẫn giao hàng'), max_length=255, blank=True)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    default = models.BooleanField(_('Default'), default=False)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return '{} Address'.format(self.full_name)
