from django.db.models import F
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render

from orders.forms import Order_Direct_Form
from orders.models import save_List, save_Item_List, Order_Item_Direct
from store.models import Product
from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    user_id = request.user.id
    savels = save_List.objects.filter(user_id=user_id)
    if request.method == "POST":
        direct_form = Order_Direct_Form(data=request.POST)
        if direct_form.is_valid():
            direct_form = direct_form.save(commit=False)
            direct_form.total_paid = basket.get_total_price()
            direct_form.save()
            order_id = direct_form.pk
            for item in basket:
                Order_Item_Direct.objects.create(order_direct_id=order_id, product=item["product"], price=item["price"],
                                                 quantity=item["qty"])
            return render(request, 'account/dashboard/order_direct.html')
    else:
        direct_form = Order_Direct_Form()
    return render(request, 'basket/summary.html', {'basket': basket, 'savels': savels, 'form': direct_form})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        Product.objects.filter(pk=product_id).update(count=F('count') + 1)
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(Product, id=product_id)
        get_product_qty = basket.get_product(product)
        if get_product_qty == 0:
            reload = 1
        else:
            reload = 0
        print(get_product_qty)
        basket.add(product=product, qty=product_qty)
        basketqty = basket.__len__()
        response = JsonResponse(
            {'qty': basketqty, 'product_id': product_id, "product_qty": product_qty, "reload": reload, })
        return response


def basket_list_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        list_save_id = int(request.POST.get('listsaveid'))
        print(list_save_id)
        item_list_save = save_Item_List.objects.filter(save_list_id=list_save_id)
        print(item_list_save)
        for item in item_list_save:
            product_id = item.product_id
            product_qty = item.quantity
            product = get_object_or_404(Product, id=product_id)
            get_product_qty = basket.get_product(product)
            if get_product_qty == 0:
                reload = 1
            else:
                reload = 0
            # print(get_product_qty)
            basket.add(product=product, qty=product_qty)
        basketqty = basket.__len__()
        response = JsonResponse({'basketqty': basketqty})
        return response


def basket_list_add_by_id(request, id):
    basket = Basket(request)
    item_list_save = save_Item_List.objects.filter(save_list_id=id)
    for item in item_list_save:
        product_id = item.product_id
        product_qty = item.quantity
        product = get_object_or_404(Product, id=product_id)
        # print(get_product_qty)
        basket.add(product=product, qty=product_qty)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)
        basketqty = basket.__len__()
        basketTotal = basket.get_total_price()
        reponse = JsonResponse({'subtotal': basketTotal, 'qty': basketqty})
        return reponse


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)
        basketqty = basket.__len__()
        basketTotal = basket.get_subtotal_price()
        reponse = JsonResponse({'qty': basketqty, 'subtotal': basketTotal})
        return reponse
