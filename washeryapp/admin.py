from django.contrib import admin

# Register your models here.
from washeryapp.models import Cleaner, Customer, Driver, Item, Invoice, InvoiceDetail, Route, WayPoint, PaymentMethod

admin.site.register(Cleaner)
admin.site.register(Customer)
admin.site.register(PaymentMethod)
admin.site.register(Driver)
admin.site.register(Item)

admin.site.register(Invoice)
admin.site.register(InvoiceDetail)

admin.site.register(Route)
admin.site.register(WayPoint)
