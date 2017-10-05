from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Cleaner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cleaner')
    name = models.CharField(max_length = 500)
    phone = models.CharField(max_length = 500)
    address = models.CharField(max_length = 500)
    latitude = models.DecimalField(max_digits=9, decimal_places = 6)
    longitude = models.DecimalField(max_digits=9, decimal_places = 6)
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
    location = models.CharField(max_length = 500, blank = True)

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
    cleaner = models.ForeignKey(Cleaner)

    created_at = models.DateTimeField(default = timezone.now)
    started_at = models.DateTimeField(blank = True, null = True)
    completed_at = models.DateTimeField(blank = True, null = True)

    def __str__(self):
        return str(self.id)


class Invoice(models.Model):
    REQUESTED = 6
    PICKEDUP = 5
    CLEANING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4
    STATUS_CHOICES = (
        (REQUESTED, "Requested"),   # Pick up request created.
        (PICKEDUP, "Picked Up"),    # Pickup waypoint completed.
        (CLEANING, "Cleaning"),     # Invoice updated with details.
        (READY, "Ready"),           # Cleaning Completed, Ready to be routed. (possibly not needed)
        (ONTHEWAY, "On the way"),   # Route started.
        (DELIVERED, "Delivered"),   # Delivery waypoint completed.
    )

    MORNING = 100
    EVENING = 101
    PERIOD_CHOICES = (
        (MORNING, "Morning"),
        (EVENING, "Evening"),
    )

    def two_day_hence():
        return timezone.now() + timezone.timedelta(days=2)

    customer = models.ForeignKey(Customer)
    cleaner = models.ForeignKey(Cleaner)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    pieces = models.IntegerField()
    status = models.IntegerField(choices = STATUS_CHOICES)
    ready_by = models.DateTimeField(default = timezone.now)
    created_at = models.DateTimeField(default = timezone.now)
    paid_on = models.DateTimeField(blank = True, null = True)

    pickup_date = models.DateTimeField()
    pickup_period = models.IntegerField(choices = PERIOD_CHOICES)
    dropoff_date = models.DateTimeField()
    dropoff_period = models.IntegerField(choices = PERIOD_CHOICES)

    def __str__(self):
        return str(self.id)

class InvoiceDetail(models.Model):
    invoice = models.ForeignKey(Invoice, related_name = 'invoice_details')
    item = models.ForeignKey(Item)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()
    piece_count = models.IntegerField()

    def __str__(self):
        return str(self.id)

class WayPoint(models.Model):
    PICKUP = 1
    DROPOFF = 2

    TYPE_CHOICES = (
        (PICKUP, "Pick up"),
        (DROPOFF, "Drop off")
    )

    cleaner = models.ForeignKey(Cleaner)
    route = models.ForeignKey(Route, related_name = 'waypoints', blank=True, null=True)
    invoice = models.ForeignKey(Invoice)    # nullable, used for drop-offs.
    waypoint_type = models.IntegerField(choices = TYPE_CHOICES)
    waypoint_order = models.IntegerField(default = 0)
    address = models.CharField(max_length=500)  # snapped from customer/invoice.
    latitude = models.DecimalField(max_digits=9, decimal_places = 6)
    longitude = models.DecimalField(max_digits=9, decimal_places = 6)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class PaymentMethod(models.Model):
    STRIPE = 1
    PAYPAL = 2
    VENDOR_CHOICES = (
        (STRIPE, "Stripe"),
        (PAYPAL, "Paypal")
    )

    customer = models.ForeignKey(Customer)
    vendor = models.IntegerField(choices = VENDOR_CHOICES)
    token = models.CharField(max_length = 500)
    # created_at = models.DateTimeField(default = timezone.now) #timestamp track latest?

    def __str__(self):
        return str(self.id)
