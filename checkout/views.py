import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render

from account.models import Address
from basket.basket import Basket
from orders.models import OrderItem, Order
from .models import DeliveryOptions


@login_required
def delivery_choices(request):
    delivery_options = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": delivery_options})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        delivery_option = int(request.POST.get('deliveryoption'))
        delivery_type = DeliveryOptions.objects.get(id=delivery_option)
        updated_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if 'purchase' not in request.session:
            session['purchase'] = {
                'delivery_id': delivery_type.id,
            }
        else:
            session['purchase']['delivery_id'] = delivery_type.id
            session.modified = True

        response = JsonResponse({'total': updated_total_price, 'delivery_price': delivery_type.delivery_price})
        return response


@login_required
def delivery_address(request):
    session = request.session
    if 'purchase' not in request.session:
        messages.success(request, 'Vui lòng chọn cài đặt giao hàng')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    if addresses:
        if 'address' not in request.session:
            session['address'] = {'address_id': str(addresses[0].id)}
        else:
            session['address']['address_id'] = str(addresses[0].id)
            session.modified = True

    return render(request, 'checkout/delivery_address.html', {'addresses': addresses})


@login_required
def post_paid(request):
    basket = Basket(request)
    addresses = Address.objects.filter(customer=request.user).order_by("-default")
    session = request.session
    delivery_option = session['purchase']['delivery_id']
    delivery_type = DeliveryOptions.objects.get(id=delivery_option)
    total_paid = basket.basket_update_delivery(delivery_type.delivery_price)
    order = Order.objects.create(
        user_id=request.user.id,
        full_name=str(addresses[0].full_name),
        email=request.user.email,
        address1=str(addresses[0].address_line),
        address2=str(addresses[0].address_line2),
        postal_code=addresses[0].postcode,
        city=addresses[0].town_city,
        phone=addresses[0].phone,
        total_paid=total_paid,
        # order_key="",
        payment_option="Post-paid",
        billing_status=False,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/poin_paid_successful.html", {})


@login_required
def payment_selection(request):
    session = request.session
    if 'address' not in request.session:
        messages.success(request, 'Vui lòng chọn cài đặt địa chỉ')
        return HttpResponseRedirect(request.META['HTTP_REFERER'])

    return render(request, 'checkout/payment_selection.html', {})


####
# PayPay
####
from paypalcheckoutsdk.orders import OrdersGetRequest
from .paypal import PayPalClient


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestorder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestorder)

    total_paid = response.result.purchase_units[0].amount.value

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        city=response.result.purchase_units[0].shipping.address.country_code,
        phone="0",
        total_paid=response.result.purchase_units[0].amount.value,
        # order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk

    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])

    return JsonResponse("Payment completed!", safe=False)


# @login_required
# def payment_complete(request):

@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})
