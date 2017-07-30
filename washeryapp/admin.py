from django.contrib import admin

# Register your models here.
from washeryapp.models import Cleaner, Customer, Driver

admin.site.register(Cleaner)
admin.site.register(Customer)
admin.site.register(Driver)
