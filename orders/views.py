from django.shortcuts import render, redirect
from django.urls import reverse

from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem
from orders.tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            cart.clear()
            order_created.s(order_id=order.id).apply_async()
            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})

            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))

    else:
        form = OrderCreateForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
