import json
import os

import torch
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.storage import default_storage
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils.text import slugify

from basket.basket import Basket
from orders.models import Order
from .filters import ProductFilter
from .forms import ContactForm
from .models import Category, Product


def product_all(request):
    basket = Basket(request)
    session = request.session
    if 'display' not in request.session:
        session['display'] = {
            'display_id': 0,
        }
    if request.user.is_authenticated:
        wishlist = Product.objects.filter(users_wishlist=request.user)
        category = Category.objects.all()
        products = Product.objects.prefetch_related('product_image').filter(is_active=True)
        my_filters = ProductFilter(request.GET, queryset=products)
        products = my_filters.qs
        return render(request, 'store/product_all.html',
                      {'products': products, 'category': category, 'wishlist': wishlist, 'myFilter': my_filters,
                       'display': session['display']['display_id'], 'basket': basket})
    else:
        category = Category.objects.all()
        products = Product.objects.prefetch_related('product_image').filter(is_active=True)
        my_filters = ProductFilter(request.GET, queryset=products)
        products = my_filters.qs
        return render(request, 'store/product_all.html',
                      {'products': products, 'category': category, 'myFilter': my_filters,
                       'display': session['display']['display_id'], 'basket': basket})


def category_list(request, category_slug=None):
    basket = Basket(request)
    print(category_slug)
    session = request.session
    if 'display' not in request.session:
        session['display'] = {
            'display_id': 0,
        }
    if request.user.is_authenticated:
        wishlist = Product.objects.filter(users_wishlist=request.user)
        category = get_object_or_404(Category, slug=category_slug)
        print(category)
        # products = Product.objects.filter(category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True))
        products = Product.objects.filter(
            category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True))
        return render(request, 'store/search_category.html',
                      {'products': products, 'category': category, 'wishlist': wishlist,
                       'display': session['display']['display_id'], 'basket': basket})
    else:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True))
        return render(request, 'store/search_category.html',
                      {'products': products, 'category': category, 'display': session['display']['display_id'],
                       'basket': basket})


def home(request):
    basket = Basket(request)
    width = 0
    count = 0
    form = ContactForm()
    orders = Order.objects.all()
    for order in orders:
        width += order.rating
        if order.isRate:
            count += 1
    if orders.count() > 0:
        width = width / orders.count()
    else:
    # Handle the case where orders count is zero
    # You can set width to a default value or perform an alternative action
        width = 0  # For example, setting width to 0
    start = width / 20
    print(start)
    print(width)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            subject = 'Active your Account'
            message = render_to_string('store/contact_email.html', {
                'user': user,
                'domain': current_site.domain,
            })
            user.email_contact(subject=subject, message=message)
            return render(request, 'store/success_contact.html')

    if request.user.is_authenticated:
        wishlist = Product.objects.filter(users_wishlist=request.user)
        products = Product.objects.prefetch_related('product_image').filter(is_active=True)
        products = products.order_by('-count')[:6]
        return render(request, 'store/index.html',
                      {'products': products, 'wishlist': wishlist, 'form': form, 'width': width, 'count': count,
                       'basket': basket, 'start': start})
    else:
        products = Product.objects.prefetch_related('product_image').filter(is_active=True)
        products = products.order_by('-count')[:6]
        return render(request, 'store/index.html',
                      {'products': products, 'form': form, 'width': width, 'count': count, 'basket': basket,
                       'start': start})


def home_img(request):
    width = 0
    count = 0
    orders = Order.objects.all()
    for order in orders:
        width += order.rating
        if order.isRate:
            count += 1
    if orders.count() > 0:
        width = width / orders.count()
    else:
    # Handle the case where orders count is zero
    # You can set width to a default value or perform an alternative action
        width = 0  # For example, setting width to 0
    
    start = width / 20
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            subject = 'Active your Account'
            message = render_to_string('store/contact_email.html', {
                'user': user,
                'domain': current_site.domain,
            })
            user.email_contact(subject=subject, message=message)
            return render(request, 'store/success_contact.html')
    if request.user.is_authenticated:
        wishlist = Product.objects.filter(users_wishlist=request.user)
        products = Product.objects.prefetch_related('product_image').filter(is_active=True)
        products = products.order_by('-count')[:6]
        return render(request, 'store/index_img.html',
                      {'products': products, 'wishlist': wishlist, 'form': form, 'width': width, 'count': count,
                       'start': start})
    else:
        products = Product.objects.prefetch_related('product_image').filter(is_active=True)
        products = products.order_by('-count')[:6]
        return render(request, 'store/index_img.html',
                      {'products': products, 'form': form, 'width': width, 'count': count, 'start': start})


def product_detail(request, slug, category_id):
    basket = Basket(request)
    session = request.session
    if 'display' not in request.session:
        session['display'] = {
            'display_id': 0,
        }
    if request.user.is_authenticated:
        Product.objects.filter(slug=slug).update(count=F('count') + 1)
        product = get_object_or_404(Product, slug=slug, is_active=True)
        wishlist = Product.objects.filter(users_wishlist=request.user)
        products = Product.objects.prefetch_related('product_image').filter(is_active=True, category_id=category_id)
        return render(request, 'store/detail.html', {'product': product, 'products': products, 'wishlist': wishlist,
                                                     'display': session['display']['display_id'], 'basket': basket})

    else:
        product = get_object_or_404(Product, slug=slug, is_active=True)
        products = Product.objects.prefetch_related('product_image').filter(is_active=True, category_id=category_id)
        return render(request, 'store/detail.html',
                      {'product': product, 'products': products, 'display': session['display']['display_id'],
                       'basket': basket})


def search(request):
    basket = Basket(request)
    session = request.session
    txt = request.GET.get('search', None)  # do some research what it does
    txt_slugify = slugify(txt)
    # slug = CharFilter(field_name='slug', lookup_expr='icontains')
    ms = "Thất bại"
    mx = "Rất tiêc không tìm thấy từ khóa "
    if 'display' not in request.session:
        session['display'] = {
            'display_id': 0,
        }
    if request.method == 'GET':  # this will be GET now
        try:
            status = Product.objects.filter(
                Q(slug__icontains=txt_slugify) |
                Q(regular_price__icontains=txt_slugify) |
                Q(product_type__slug__icontains=txt_slugify) |
                Q(category__slug__icontains=txt_slugify)
            )
            if status:
                ms = "Thành công"
                mx = "Nếu không phải là "
        except:
            status = ""

        if request.user.is_authenticated:
            wishlist = Product.objects.filter(users_wishlist=request.user)
            return render(request, "./store/search_result.html",
                          {"products": status, "ms": ms, "mx": mx, 'wishlist': wishlist, "label": txt,
                           'display': session['display']['display_id'], 'basket': basket})
        else:
            return render(request, "./store/search_result.html",
                          {"products": status, "ms": ms, "mx": mx, "label": txt,
                           'display': session['display']['display_id'], 'basket': basket})
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def search_img(request):
    basket = Basket(request)
    session = request.session
    if 'display' not in request.session:
        session['display'] = {
            'display_id': 0,
        }
    if request.method == "POST":
        #
        # Django image API
        #
        ms = "Thất bại"
        mx = "Không thể nhận dạng ra kết quả phù hợp"
        file = request.FILES["imageFile"]
        print(file)
        file_name = default_storage.save(file.name, file)
        file_url = default_storage.path(file_name)
        print(file_url)
        model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt')  # local model

        # Image
        img = file_url

        # Inference
        results = model(img, size=640)
        # results_name = default_storage.save(file.name, results)
        result = results.pandas().xyxy[0].to_json(orient="records")
        print(result)
        parsed = json.loads(result)
        # f = json.dumps(parsed, indent=4)
        # print(f)
        try:
            label = parsed[0]['name']
            path_save = str('assets/home/img/exp/' + label)
            print(path_save)
            results.save('assets/home/img/exp/' + label)
            path_save1 = str('home/img/exp/' + label + '/' + file_name)
            ms = ""
            mx = "Nếu không phải là "
        except:
            return render(request, "./store/search_result_img.html", {"ms": ms, "mx": mx})
        if request.user.is_authenticated:
            wishlist = Product.objects.filter(users_wishlist=request.user)
            category = get_object_or_404(Category, slug=label)
            # products = Product.objects.filter(category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True))
            products = Product.objects.filter(
                category__in=Category.objects.get(slug=label).get_descendants(include_self=True))
            return render(request, "./store/search_result_img.html",
                          {"products": products, "name_path": path_save1, 'wishlist': wishlist, "label": label,
                           "ms": ms, "mx": mx,
                           "rs": category, 'display': session['display']['display_id'], 'basket': basket})
        else:
            category = get_object_or_404(Category, slug=label)
            products = Product.objects.filter(
                category__in=Category.objects.get(slug=label).get_descendants(include_self=True))
            return render(request, "./store/search_result_img.html",
                          {"products": products, "label": label, "name_path": path_save1, "ms": ms, "mx": mx,
                           "rs": category, 'display': session['display']['display_id'], 'basket': basket})
        # print(label)
    #
    # else:
    #     return render(request, "store/index_img.html")
    return redirect('store:index_img')


def display(request):
    # Display.objects.filter(customer=request.user, default=True).update(default=False)
    # Address.objects.filter(pk=id, customer=request.user).update(default=True)
    session = request.session
    if 'display' not in request.session:
        session['display'] = {
            'display_id': 0,
        }
    elif session['display']['display_id'] == 0:
        session['display']['display_id'] = 1
        session.modified = True
    else:
        session['display']['display_id'] = 0
        session.modified = True
    previous_url = request.META.get('HTTP_REFERER')
    if 'shop' in previous_url:
        return HttpResponseRedirect(request.META['HTTP_REFERER'])
    return redirect('store:product_all')
