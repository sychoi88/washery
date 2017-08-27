from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Cleaner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cleaner')
    name = models.CharField(max_length = 500)
    phone = models.CharField(max_length = 500)
    address = models.CharField(max_length = 500)
    logo = models.ImageField(upload_to='cleaner_logo/', blank=False)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'customer')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name = 'driver')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=500, blank=True)
    address = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Item(models.Model):
    cleaner = models.ForeignKey(Cleaner)
    name = models.CharField(max_length=500)
    short_description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='item_images/', blank=False)
    piece_count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Route(models.Model):
    driver = models.ForeignKey(Driver)

    def __str__(self):
        return str(self.id)

class Invoice(models.Model):
    CLEANING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (CLEANING, "Cleaning"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    )

    customer = models.ForeignKey(Customer)
    cleaner = models.ForeignKey(Cleaner)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    created_at = models.DateTimeField(default = timezone.now )

    def __str__(self):
        return str(self.id)

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, related_name = 'invoice_details')
    item = models.ForeignKey(Item)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class Stop(models.Model):
    PICKUP = 1
    DROPOFF = 2

    TYPE_CHOICES = (
        (PICKUP, "Pick up"),
        (DROPOFF, "Drop off")
    )

    route = models.ForeignKey(Route, related_name = 'stops')
    customer = models.ForeignKey(Customer)  # nullable, used for pick-ups.
    invoice = models.ForeignKey(Invoice)    # nullable, used for drop-offs.

    address = models.CharField(max_length=500)  # snapped from customer/invoice.
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)
