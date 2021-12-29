# from django.conf import settings
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.core.mail import send_mail

# -*- coding: utf-8 -*-
class Category(MPTTModel):
    """
    Category Table implimented with MPTT.
    """
    name = models.CharField(verbose_name=_('Category Name'), help_text=_('Bắt buộc và duy nhất'), max_length=255,
                            unique=True, )
    slug = models.SlugField(verbose_name=_('Category safe URL'), null=True, max_length=255, unique=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def get_absolute_url(self):
        return reverse('store:category_list', args=[self.slug])

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.name)
    #     super(Category, self).save(*args, **kwargs)


class ProductType(models.Model):
    """
    ProductType Table will provide a list of the different types
    of products that are for sale.
    """
    name = models.CharField(verbose_name=_('Product Name'), help_text=_('Bắt buộc'), max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Product Type')
        verbose_name_plural = _('Product Types')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(ProductType, self).save(*args, **kwargs)


class ProductSpecification(models.Model):
    """
   The Product Specification Table contains product
   specifiction or features for the product types.
   """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_('Name'), help_text=_('Bắt buộc'), max_length=255)

    class Meta:
        verbose_name = _('Product Specification')
        verbose_name_plural = _('Product Specifications')

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The Product table contining all product items.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, related_name='category_id', on_delete=models.RESTRICT)
    title = models.CharField(verbose_name=_('title'), help_text=_('Bắt buộc'), max_length=255)
    description = models.TextField(verbose_name=_('description'), help_text=_('Không bắt buộc'), blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    regular_price = models.DecimalField(
        verbose_name=_('Regular price'), help_text=_('Tối đa 99999.999'),
        error_messages={
            'name': {
                'max_length': _('Giá sản phẩm phải từ 0 đến 99999.999'),
            },
        },
        max_digits=8,
        decimal_places=3,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Discount price"),
        help_text=_("Tối đa 99999.999"),
        error_messages={
            "name": {
                "max_length": _("Giảm từ 0 đến 99999.999"),
            },
        },
        max_digits=8,
        decimal_places=3,
    )
    is_active = models.BooleanField(
        verbose_name=_('Product Visibility'),
        help_text=_('Hiển thị sản phẩm'),
        default=True,
    )
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='users_wishlist', blank=True)
    count = models.IntegerField(default=0, blank=True)

    class Meta:
        ordering = ('-count', '-created_at',)
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug, self.category_id])

    def get_id(self):
        return self.id

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)


class ProductSpecificationValue(models.Model):
    """
    The Product Specification Value table holds each of the
    products individual specification or bespoke features.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    specification = models.ForeignKey(ProductSpecification, on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_('value'),
        help_text=_('Thông số sản phẩm (tối đa 255 kí tự)'),
        max_length=255,
    )

    class Meta:
        verbose_name = _('Product Specification Value')
        verbose_name_plural = _('Product Specification Values')

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    """
    The Product Image table.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_image')
    image = models.ImageField(
        verbose_name=_('image'),
        help_text=_('Tải lên một hình ảnh'),
        upload_to='images/',
        default='images/default.png',
    )
    alt_text = models.CharField(
        verbose_name=_('Alternative text'),
        help_text=_('Please add alternative text'),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')


class Contact(models.Model):
    email = models.EmailField()
    fullname = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def email_contact(self, subject, message):
        send_mail(
            subject,
            message,
            'l@1.com',
            [self.email],
            fail_silently=False,
        )

    def __str__(self):
        return self.email

