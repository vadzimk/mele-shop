from django.contrib import admin

from orders.models import OrderItem, Order


# will be displayed inline with the Order model in the admin panel
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    # an inline allows to include a model on the same edit page as its related model
    inlines = [OrderItemInline]
