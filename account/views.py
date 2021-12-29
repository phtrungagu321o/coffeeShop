from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from basket.basket import Basket
from orders.models import Order, save_List, save_Item_List
from orders.views import user_orders
from store.models import Product
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import Customer, Address
from .token import account_activation_token


@login_required
def wishlist(request):
    products = Product.objects.filter(users_wishlist=request.user)
    return render(request, 'account/dashboard/user_wish_list.html', {'wishlist': products})


@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    if product.users_wishlist.filter(id=request.user.id).exists():
        product.users_wishlist.remove(request.user)
        messages.success(request, "Đã xóa <span style='color:red;'>" + product.title + "</span> ra khỏi ")
    else:
        product.users_wishlist.add(request.user)
        messages.success(request, "Đã thêm <span style='color:red;'>" + product.title + "</span> vào ")
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'account/dashboard/dashboard.html', {'orders': orders})


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)

        if user_form.is_valid():
            user_form.save()

    else:
        user_form = UserEditForm(instance=request.user)

    return render(request, 'account/dashboard/edit_details.html', {'user_form': user_form})


@login_required
def delete_user(request):
    user = Customer.objects.get(name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirm')


def account_register(request):
    if request.user.is_authenticated:
        return redirect("account:dashboard")

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.name = registerForm.cleaned_data['user_name']
            user.email = registerForm.clean_email()
            user.set_password(registerForm.clean_password2())
            user.is_active = False
            user.save()

            #   setup email
            current_site = get_current_site(request)
            subject = 'Active your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'dashboard': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html', {'form': registerForm})
    else:
        registerForm = RegistrationForm()
    return render(request, 'account/registration/register.html', {'form': registerForm})


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except():
        pass
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')


# Addresses
@login_required
def view_address(request):
    addresses = Address.objects.filter(customer=request.user)
    return render(request, 'account/dashboard/addresses.html', {'addresses': addresses})


@login_required
def add_address(request):
    edit = 'Thêm địa chỉ'
    if request.method == 'POST':
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            messages.success(request,
                             "Đã thêm địa chỉ của <span style='color:red;'>" + address_form.address_line + "</span> vào tài khoản")
            return HttpResponseRedirect(reverse('account:addresses'))
    else:
        address_form = UserAddressForm()
    return render(request, 'account/dashboard/edit_addresses.html', {'form': address_form, 'edit': edit})


@login_required
def edit_address(request, id):
    edit = 'Sửa địa chỉ'
    if request.method == 'POST':
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            previous_url = request.META.get('HTTP_REFERER')

            if 'delivery_address' in previous_url:
                return HttpResponseRedirect(reverse('checkout:delivery_address'))
            address_form = get_object_or_404(Address, pk=id, customer=request.user)
            messages.success(request,
                             "Đã sửa địa chỉ <span style='color:red;'>" + address_form.address_line + "</span> thành công")
            return HttpResponseRedirect(reverse('account:addresses'))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, 'account/dashboard/edit_addresses.html', {'form': address_form, 'edit': edit})


@login_required
def delete_address(request, id):
    address_form = get_object_or_404(Address, pk=id, customer=request.user)
    messages.success(request,
                     "Đã xóa địa chỉ <span style='color:red;'>" + address_form.address_line + "</span> thành công")
    Address.objects.filter(pk=id, customer=request.user).delete()
    return redirect('account:addresses')


@login_required
def delete_order(request, id):
    order = get_object_or_404(Order, id=id)
    messages.success(request,
                     "Đã xóa thành công đơn hàng " + order.order_key)
    order.delete()
    return redirect('account:user_not_orders')


@login_required
def set_default(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    address_form = get_object_or_404(Address, pk=id, customer=request.user)
    previous_url = request.META.get('HTTP_REFERER')
    messages.success(request,
                     "Đã cài địa chỉ <span style='color:red;'>" + address_form.address_line + "</span> làm địa chỉ mặc định")
    if 'delivery_address' in previous_url:
        return redirect('checkout:delivery_address')

    return redirect("account:addresses")


@login_required
def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return render(request, 'account/dashboard/user_orders.html', {'orders': orders})


@login_required
def save_list(request):
    user_id = request.user.id
    savels = save_List.objects.filter(user_id=user_id)
    return render(request, 'account/dashboard/user_save_list.html', {'savels': savels})


@login_required
def user_save_list(request):
    basket = Basket(request)
    session = request.session
    total_paid = basket.get_total_price()
    savels = save_List.objects.create(
        user_id=request.user.id,
        total_paid=total_paid,
    )
    save_id = savels.pk

    for item in basket:
        save_Item_List.objects.create(save_list_id=save_id, product=item["product"], price=item["price"],
                                      quantity=item["qty"])
    messages.success(request,
                     "Đã lưu thành công đơn hàng, mua thêm ")
    return redirect('account:save_list')


@login_required
def delete_save(request, id):
    savels = get_object_or_404(save_List, pk=id)
    messages.success(request,
                     "Đã xóa <span style='color:red;'>"+savels.title+"</span> thành công, mua thêm ")
    save_List.objects.filter(pk=id).delete()
    return redirect('account:save_list')


@login_required
def user_not_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=False)
    return render(request, 'account/dashboard/user_not_orders.html', {'orders': orders})


@login_required
def rating(request, id):
    orders = Order.objects.filter(pk=id).filter(billing_status=True)
    print(orders)
    print(id)
    return render(request, 'account/dashboard/rating.html', {'orders': orders})


@login_required
def rating_ditgis(request, id, rate):
    orders = Order.objects.filter(pk=id).filter(billing_status=True)
    orders.update(rating=rate * 20)
    orders.update(isRate=True)
    messages.success(request,
                     "Cảm ơn bạn đã đánh giá cho đơn hàng, bạn có thể xem thêm sản phẩm ")
    return redirect('account:user_orders')


@login_required
def val_order(request, id):
    orders = Order.objects.filter(pk=id).filter(billing_status=True)
    if request.method == 'POST':
        txt = request.POST.get('problem', None)
        Order.objects.filter(pk=id).filter(billing_status=True).update(Problem=txt)
        order = get_object_or_404(Order, pk=id, billing_status=True)
        messages.success(request,
                         "Vấn đề của bạn với đơn hàng <span style='color:red;'>" + order.order_key + "</span> đã được gửi, cảm ơn bạn đã quan tâm, xem thêm sản phẩm ")
        return redirect('account:user_orders')
    return render(request, "account/dashboard/val_user_orders.html", {'orders': orders})


@login_required
def edit_title_save(request, id):
    if request.method == 'POST':
        txt = request.POST.get('save_list-title', None)
        save_List.objects.filter(pk=id).update(title=txt)
        messages.success(request,
                         "Đã đặt tên giỏ hàng thành công!!!, xem thêm sản phẩm")
    return redirect('account:save_list')
