import csv
import datetime

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.http import HttpResponse
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


# https://docs.djangoproject.com/en/4.1/howto/outputting-csv/
def export_to_csv(modeladmin: ModelAdmin, request, queryset):
    """ custom admin action to download a list from model as csv file """
    opts = modeladmin.model._meta
    content_disposition = f'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition  # add header
    writer = csv.writer(response)  # csv writer will write to the response object
    fields = [field for field in opts.get_fields()
              if not field.many_to_many and not field.one_to_many]
    # write the first rew with header info
    writer.writerow([field.verbose_name for field in fields])
    # write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


export_to_csv.short_description = 'Export to CSV'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email',
                    'address', 'postal_code', 'city', 'paid',
                    order_payment, 'created', 'updated']
    list_filter = ['paid', 'created', 'updated']
    # an inline allows to include a model on the same edit page as its related model
    inlines = [OrderItemInline]
    actions = [export_to_csv]
