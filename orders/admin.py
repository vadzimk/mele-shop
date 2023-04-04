from django.contrib import admin
from django.utils.safestring import mark_safe

from orders.models import OrderItem, Order


# will be displayed inline with the Order model in the admin panel
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''


# https://stackoverflow.com/questions/338101/python-function-attributes-uses-and-abuses
order_payment.short_description = 'Stripe payment'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    order_payment, 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    # an inline allows to include a model on the same edit page as its related model
    inlines = [OrderItemInline]
