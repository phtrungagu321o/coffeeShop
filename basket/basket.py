import decimal
from decimal import Decimal

from django.conf import settings

from checkout.models import DeliveryOptions
from store.models import Product


class Basket():
    # cung cấp hành vi mặc định có thể được kế thừa hoặc ghi đè
    def __init__(self, request):
        self.VAT = decimal.Decimal('23.030')
        self.session = request.session
        basket = self.session.get(settings.BASKET_SESSION_ID)
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)
        # Adding and updating the users basket session data
        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {'price': str(product.regular_price), 'qty': qty}

        self.save()

    def get_product(self, product):
        product_id = str(product.id)
        if product_id in self.basket:
            quantity = self.basket[product_id]['qty']
            return quantity
        else:
            return 0

    def __iter__(self):

        # Collect the product_id in the session data to query the database
        #  and return products
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def __len__(self):
        return sum(item['qty'] for item in self.basket.values())

    def get_subtotal_price(self):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        return subtotal

    def get_delivery_price(self):
        newprice = 0.000
        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
        return newprice

    def get_total_price(self):
        newprice = 0.000
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
        total = subtotal + Decimal(newprice)
        return total

    def get_total_qty(self):
        return sum(item['qty'] for item in self.basket.values())

    def delete(self, product):
        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]

        self.save()

    def update(self, product, qty):
        product_id = str(product)
        qty = qty

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty

        self.save()

    def basket_update_delivery(self, deliveryprice=0):
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
        total = subtotal + Decimal(deliveryprice)
        return total

    def price_convert_vnd(self):
        newprice = 0.000
        subtotal = sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())

        if 'purchase' in self.session:
            newprice = DeliveryOptions.objects.get(id=self.session['purchase']['delivery_id']).delivery_price
        total = subtotal + Decimal(newprice)
        total_convert = decimal.Decimal(total) / self.VAT
        return total_convert

    def clear(self):
        del self.session[settings.BASKET_SESSION_ID]
        del self.session['address']
        del self.session['purchase']
        self.save()

    def save(self):
        self.session.modified = True
