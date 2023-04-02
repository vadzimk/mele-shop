from decimal import Decimal

from django.conf import settings

from shop.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}  # create empty cart
        self.cart = cart

    def add(self,
            product,
            quantity=1,
            override_quantity=False):
        """ adds products to cart or update quantity """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """ mark session as modified and save """
        self.session.modified = True

    def remove(self, product):
        """ Remove a product from the cart """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()  # update session

    def __iter__(self):
        """ iterate cart as list """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """ count all items in the cart """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """ remove cart from session """
        del self.session[settings.CART_SESSION_ID]
        self.save()
