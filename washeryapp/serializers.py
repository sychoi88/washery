from rest_framework import serializers

from washeryapp.models import Cleaner, \
    Item, \
    Customer, \
    Driver, \
    Invoice, \
    InvoiceDetail, \
    Route, \
    WayPoint

class CleanerSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, cleaner):
        request = self.context.get('request')
        logo_url = cleaner.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Cleaner
        fields = ("id", "name", "phone", "address", "logo")

class ItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, item):
        request = self.context.get('request')
        image_url = item.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Item
        fields = ("id", "name", "short_description", "image", "price", "piece_count")

# INVOICE SERIALIZER
class InvoiceCustomerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Customer
        fields = ("id", "name", "avatar", "phone", "address")


class InvoiceDriverSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source="user.get_full_name")

    class Meta:
        model = Driver
        fields = ("id", "name", "avatar", "phone", "address")


class InvoiceCleanerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cleaner
        fields = ("id", "name", "phone", "address")


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "price", "piece_count")


class InvoiceDetailSerializer(serializers.ModelSerializer):
    item = InvoiceItemSerializer()

    class Meta:
        model = InvoiceDetail
        fields = ("id", "item", "quantity", "sub_total", "piece_count")

class InvoiceSerializer(serializers.ModelSerializer):
    customer = InvoiceCustomerSerializer()
    cleaner = InvoiceCleanerSerializer()
    invoice_details = InvoiceDetailSerializer(many= True)
    status = serializers.ReadOnlyField(source = "get_status_display")

    class Meta:
        model = Invoice
        fields = ("id", "customer", "cleaner", "invoice_details", "total", "status", "address", "pieces")

class WayPointSerializer(serializers.ModelSerializer):
    invoice = InvoiceSerializer()
    customer = InvoiceCustomerSerializer()
    waypoint_type = serializers.ReadOnlyField(source = "get_waypoint_type_display")


    class Meta:
        model = WayPoint
        fields = ("id", "invoice", "customer", "address","waypoint_type", "completed_at")

class RouteSerializer(serializers.ModelSerializer):
    driver = InvoiceDriverSerializer()
    waypoints = WayPointSerializer(many=True)

    class Meta:
        model = Route
        fields = ("id", "driver", "waypoints")
