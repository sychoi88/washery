import json

import datetime
from django.utils import timezone
from django.http import JsonResponse
from oauth2_provider.models import AccessToken
from django.views.decorators.csrf import csrf_exempt

from washeryapp.models import Cleaner, Item, Invoice, InvoiceDetail, Route, WayPoint, Driver
from washeryapp.serializers import CleanerSerializer, ItemSerializer, InvoiceSerializer, RouteSerializer, WayPointSerializer, RouteDriverSerializer

import stripe
from washery.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY

############
# CUSTOMERS
############
def customer_get_cleaners(request):
    cleaners = CleanerSerializer(
        Cleaner.objects.all().order_by("-id"),
        many=True,
        context = {"request": request}
    ).data

    return JsonResponse({"cleaners": cleaners})

def customer_get_items(request, cleaner_id):
    items = ItemSerializer(
        Item.objects.filter(cleaner_id = cleaner_id).order_by("-id"),
        many=True,
        context = {"request": request}
    ).data

    return JsonResponse({"items": items})

# POST - Request a pick up by creating a empty invoice.
@csrf_exempt
def customer_request_invoice(request):
    """
        params:
            access_token
            cleaner_id
            address
            pickup_date
            pickup_period
            dropoff_date
            dropoff_period
        return:
            {"status": "success"}
    """
    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get customer
        customer = access_token.user.customer

        # Check whether customer has any invoice that is not pickedup
        if Invoice.objects.filter(customer = customer, status = Invoice.REQUESTED):
            return JsonResponse({"status": "failed", "error": "You already have a pick up request."})

        # Check Address
        if not request.POST["address"]:
            return JsonsResponse({"status": "failed", "error": "Address is required."})

        # Check Pickup_Date and Pick_Period
        if not (request.POST["pickup_date"] or request.POST["pickup_period"]):
            return JsonsResponse({"status": "failed", "error": "Pckup Date and Pickup Period is required"})

        # Check Dropoff_Date and Dropoff_Period
        if not (request.POST["dropoff_date"] or request.POST["dropoff_period"]):
            return JsonsResponse({"status": "failed", "error": "Dropoff Date and Dropoff Period is required"})

        invoice = Invoice.objects.create(
            customer = customer,
            cleaner_id = request.POST["cleaner_id"],
            address = request.POST["address"],
            total = 0,
            pieces = 0,
            status = Invoice.REQUESTED,
            pickup_date = timezone.make_aware(datetime.datetime.strptime(request.POST["pickup_date"], "%m/%d/%Y"), timezone.get_current_timezone()),
            pickup_period = request.POST["pickup_period"],
            dropoff_date = timezone.make_aware(datetime.datetime.strptime(request.POST["dropoff_date"], "%m/%d/%Y"), timezone.get_current_timezone()),
            dropoff_period = request.POST["dropoff_period"],
        )

        # CREATE WAYPOINT HERE AS WELL HERE!!!!!!!!!!!!!!!!!!!!!!!!!!

        return JsonResponse({"status": "success"})

# POST - Update invoice with details.
def cleaner_update_invoice_new(request):

    if request.method == "POST":

        jsonInvoice = json.loads(request.POST.get('invoice'))

        invoice = Invoice.objects.get(cleaner=request.user.cleaner, id = jsonInvoice["invoice_id"])

        if not invoice.status == Invoice.PICKEDUP:
            return JsonResponse({"status": "failed", "error": "Invoice cannot be updated."})

        # Get Invoice Details
        invoice_details = json.loads(jsonInvoice["invoice_details"])

        invoice_total = 0
        invoice_pieces = 0
        for item in invoice_details:
            invoice_total += Item.objects.get(id=item["item_id"]).price * item["quantity"]
            invoice_pieces += Item.objects.get(id=item["item_id"]).piece_count * item["quantity"]

        if len(invoice_details) > 0:
            # Step 1 - Update Invoice (status, total, pieces)
            invoice.status = Invoice.CLEANING
            invoice.total = invoice_total
            invoice.pieces = invoice_pieces

            # Step 2 - Create Invoice Details
            for item in invoice_details:
                InvoiceDetail.objects.create(
                    invoice = invoice,
                    item_id = item["item_id"],
                    quantity = item["quantity"],
                    sub_total = Item.objects.get(id=item["item_id"]).price * item["quantity"],
                    piece_count = Item.objects.get(id=item["item_id"]).piece_count * item["quantity"],
                )
            invoice.save()

            return JsonResponse({"status": "success"})
        #
        # print("CHECK THIS OUT:##################################")
        # print(invoice['invoice_id'])
        # print("AND THIS OUT:##################################")
        # for detail in invoice['invoice_details']:
        #     print("item_id: " + str(detail['item_id']) +", quantity: " + str(detail['quantity']))

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "fail"})


@csrf_exempt
def cleaner_update_invoice(request):
    """
        params:
            access_token
            invoice_id
            invoice_details (json format), example:
                [{"item_id":1, "quantity":2}, {"item_id":2, "quantity": 1}]
            stripe_token
        return:
            {"status": "success"}
    """
    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get customer
        customer = access_token.user.customer

        # Get Invoice
        if Invoice.objects.filter(id = request.POST["invoice_id"]).last():

            invoice = Invoice.objects.filter(id = request.POST["invoice_id"]).last()
            if not invoice.status == Invoice.PICKEDUP:
                return JsonResponse({"status": "failed", "error": "Invoice cannot be updated."})

            # Get Invoice Details
            invoice_details = json.loads(request.POST["invoice_details"])

            invoice_total = 0
            invoice_pieces = 0
            for item in invoice_details:
                invoice_total += Item.objects.get(id=item["item_id"]).price * item["quantity"]
                invoice_pieces += Item.objects.get(id=item["item_id"]).piece_count * item["quantity"]

            if len(invoice_details) > 0:
                # Step 1 - Update Invoice (status, total, pieces)
                invoice.status = Invoice.CLEANING
                invoice.total = invoice_total
                invoice.pieces = invoice_pieces

                # Step 2 - Create Invoice Details
                for item in invoice_details:
                    InvoiceDetail.objects.create(
                        invoice = invoice,
                        item_id = item["item_id"],
                        quantity = item["quantity"],
                        sub_total = Item.objects.get(id=item["item_id"]).price * item["quantity"],
                        piece_count = Item.objects.get(id=item["item_id"]).piece_count * item["quantity"],
                    )
                invoice.save()

                return JsonResponse({"status": "success"})

# Create an Invoice (this bypasses the request and creates and invoice directly)
@csrf_exempt
def customer_add_invoice(request):
    """
        params:
            access_token
            cleaner_id
            address
            invoice_details (json format), example:
                [{"item_id":1,"quantity":2}, {"item_id":2,"quantity":1}]
            stripe_token

        return:
            {"status": "success"}
    """
    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get profile
        customer = access_token.user.customer

        # Check whether customer has any invoice that is not delivered
        if Invoice.objects.filter(customer = customer).exclude(status = Invoice.DELIVERED):
            return JsonResponse({"status": "failed", "error": "Your last invoice must be completed."})

        # Check Address
        if not request.POST["address"]:
            return JsonsResponse({"status": "failed", "error": "Address is required."})

        # Get Invoice Details
        invoice_details = json.loads(request.POST["invoice_details"])

        invoice_total = 0
        piece_count = 0
        for item in invoice_details:
            invoice_total += Item.objects.get(id=item["item_id"]).price * item["quantity"]
            piece_count += Item.objects.get(id=item["item_id"]).piece_count * item["quantity"]

        if len(invoice_details) > 0:
            # Step 1 - Create an Invoice
            invoice = Invoice.objects.create(
                customer = customer,
                cleaner_id = request.POST["cleaner_id"],
                total = invoice_total,
                pieces = piece_count,
                status = Invoice.CLEANING,
                address = request.POST["address"],
                ready_by = timezone.now()
            )

            # Step 2 - Create Invoice Details
            for item in invoice_details:
                InvoiceDetail.objects.create(
                    invoice = invoice,
                    item_id = item["item_id"],
                    quantity = item["quantity"],
                    sub_total = Item.objects.get(id=item["item_id"]).price * item["quantity"],
                    piece_count = Item.objects.get(id=item["item_id"]).piece_count * item["quantity"],
                )

            return JsonResponse({"status": "success"})

@csrf_exempt
# POST update invoice with stripe charge.
def customer_update_payment(request):
    """
        params:
            access_token
            invoice_id
            stripe_token
        return:
            {"status": "success"}
    """
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    invoice = Invoice.objects.get(
        customer = customer,
        id=request.POST["invoice_id"],
    )

    if invoice == None:
        return JsonResponse({"status": "failed", "error": "Invoice not found."})

    # if not invoice.paid_on == None:
    #     return JsonResponse({"status": "failed", "error": "Invoice is already paid."})

    # Get Stripe token.
    stripe_token = request.POST["stripe_token"]

    # Step 1: Create a charge: this will charge customer's card
    charge = stripe.Charge.create(
        amount = invoice.total*100, # Amount in cents.
        currency = "usd",
        source = stripe_token,
        description = "Washery Invoice",
    )

    if charge.status != "failed":
        invoice.paid_on = timezone.now()
        invoice.save()
        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "failed", "error": "Failed connect to Stripe."})

def customer_get_latest_invoice(request):
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer
    invoice = InvoiceSerializer(Invoice.objects.filter(customer = customer).last()).data

    return JsonResponse({"invoice": invoice})

# GET params: access_token
def customer_driver_location(request):
    return JsonResponse({"status": "warning", "error": "You must get driver's location based on the driver's route. if the driver is on your waypoint, then show location."})
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer

    # Get driver's location related to this customer's current invoice.
    current_invoice = Invoice.objects.filter(customer = customer, status = Invoice.ONTHEWAY).last()
    location = current_invoice.driver.location

    return JsonResponse({"location": location})

@csrf_exempt
# POST params: access_token
def customer_payment_method_update(request):
    """
        params:
            access_token
            stripe_id
        return:
            {"status": "Success"}
    """
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    customer = access_token.user.customer

    # Update payment_method

    return JsonResponse({"warning": "Not implemented."})


############
# CLEANER
############
def cleaner_invoice_notification(request, last_request_time):
    notification = Invoice.objects.filter(cleaner = request.user.cleaner,
    created_at__gt = last_request_time).count()

    return JsonResponse({"notification": notification})

def cleaner_get_items(request):
    pos_items = ItemSerializer(
        Item.objects.filter(cleaner=request.user.cleaner).order_by("-id"),
        many=True,
        context = {"request": request}
    ).data

    return JsonResponse({"pos_items": pos_items})

def cleaner_update_route(request):
    if request.method == "POST":

        jsonRoute = json.loads(request.POST.get('route'))
        if len(jsonRoute["waypoints"]) < 1:
            return JsonResponse({"status":"fail", "error": "waypoints is empty."})

        print("aasdfasdfasdfasdf: " + str(jsonRoute))

        try:
            print('updating existing')
            route = Route.objects.get(cleaner=request.user.cleaner, id = jsonRoute["route_id"])

            # unlink waypoint from route.
            for wp in route.waypoints.all():
                wp.route = None
                wp.waypoint_order = 0
                wp.save()

        except Route.DoesNotExist:
            print("creating new.")
            print("cleanerId" + str(request.user.cleaner.id))
            route = Route.objects.create(
                cleaner_id = request.user.cleaner.id,
                driver_id = jsonRoute["driver_id"]
            )

        # Get Waypoints
        waypoints = jsonRoute["waypoints"]

        # connect waypoint to route.
        for item in waypoints:
            waypoint = WayPoint.objects.get(cleaner = request.user.cleaner, id = item["id"])
            waypoint.route = route
            waypoint.waypoint_order = item["wp_order"]
            waypoint.save()

        return JsonResponse({"status": "success"})

    return JsonResponse({"status": "fail", "error": "message here."})

def cleaner_routeToEdit(request, route_id=0):

    print(route_id)
    print("++++++++++++++++++++++++++++++++++++")
    cleaner = CleanerSerializer(
            request.user.cleaner,
            context = {"request": request}

        ).data

    try:
        routeObj = Route.objects.get(cleaner = request.user.cleaner, id = route_id)
        route = RouteSerializer(
            routeObj
        ).data

    except Route.DoesNotExist:
        route = None

    unRouted =None

    unRouted = WayPointSerializer(
        WayPoint.objects.filter(cleaner = request.user.cleaner, route_id__isnull = True),
        many = True,
        context={"request": request}
    ).data
    drivers = RouteDriverSerializer(
        Driver.objects,
        many=True,
        context={"request": request}
    ).data

    return JsonResponse({"cleaner": cleaner, "route": route, "unrouted": unRouted, "drivers": drivers})

############
# DRIVERS
############

def driver_get_ready_invoices(request):     # require access_token to authenticate.
    invoices = InvoiceSerializer(
        Invoice.objects.filter(status = Invoice.READY).order_by("-id"),
        many = True
    ).data

    return JsonResponse({"invoices": invoices})

@csrf_exempt
# POST params: access_token, invoice_id
def driver_pick_invoice(request):
    return JsonResponse({"status": "warning", "error": "Drivers don't pick up invoices.  Apply this logic for routes."})
    # Drivers don't pick up invoices.  Apply this logic for routes.
    if request.method == "POST":
        # Get token
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        # Get Driver
        driver = access_token.user.driver

        # Check if driver can only pick up one invoice at the same time
        if Invoice.objects.filter(driver = driver).exclude(status = Invoice.ONTHEWAY):
            return JsonResponse({"status": "failed", "error": "You can only pick one invoice at the same time."})

        try:
            invoice = Invoice.objects.get(
                id=request.POST["invoice_id"],
                driver = None,
                status = Invoice.READY
            )
            invoice.driver = driver # assign the driver.
            invoice.status = Invoice.ONTHEWAY
            invoice.picked_at = timezone.now()
            invoice.save()

            return JsonResponse({"status":"success"})

        except Invoice.DoesNotExist:
            return JsonResponse({"status": "failed", "error": "This invoice has been picked up by another driver."})

    return JsonResponse({})

# GET params: access_token
def driver_get_latest_invoice(request):
    return JsonResponse({"status": "warning", "error": "Drivers should see their latest route.  Apply this logic for routes."})

    # Get token
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    invoice = InvoiceSerializer(
        Invoice.objects.filter(driver = driver).order_by("picked_at").last()
    ).data

    return JsonResponse({"invoice": invoice })

@csrf_exempt
# POST params: access_token, invoice_id
def driver_complete_invoice(request):
    return JsonResponse({"status": "warning", "error": "Drivers should complete their waypoints.  Apply this logic for waypoints."})

    # Get token
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    invoice = Invoice.objects.get(id = request.POST["invoice_id"], driver = driver)
    invoice.status = Invoice.DELIVERED
    invoice.save()

    return JsonResponse({"status": "success"})

# GET params: access_token
def driver_get_revenue(request):
    return JsonResponse({"status": "warning", "error": "Drivers should see their revenue based on their routes not the invoices.  Apply this logic for routes and invoices."})

    # Get token
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    from datetime import timedelta

    revenue = {}
    today = timezone.now()
    current_weekdays = [today + timedelta(days=i) for i in range(0-today.weekday(), 7-today.weekday())]

    for day in current_weekdays:
        invoices = Invoice.objects.filter(
            driver = driver,
            status = Invoice.DELIVERED,
            created_at__year = day.year,
            created_at__month = day.month,
            created_at__day = day.day
        )

        revenue[day.strftime("%a")] = sum(invoice.total for invoice in invoices)

    return JsonResponse({"revenue": revenue})

@csrf_exempt
# POST - params: access_token, "lat,lng"
def driver_update_location(request):
    if request.method == "POST":
        access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
            expires__gt = timezone.now())

        driver = access_token.user.driver

        # Set location string => database
        driver.location = request.POST["location"]
        driver.save()

        return JsonResponse({"status": "success"})

# GET - params: access_token
def driver_get_latest_route(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.GET.get("access_token"),
        expires__gt = timezone.now())

    driver = access_token.user.driver

    route = RouteSerializer(
        Route.objects.filter(driver = driver).order_by("created_at").last()
    ).data

    return JsonResponse({"route": route })

@csrf_exempt
# POST - params: access_token, waypoint_id
def driver_complete_waypoint(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    # Get driver
    driver = access_token.user.driver

    # Get waypoint
    waypoint = WayPoint.objects.get(id = request.POST["waypoint_id"])

    if waypoint.completed_at is not None:
        return JsonResponse({"status": "failed", "error": "waypoint already completed."})

    # complete waypoint
    completed_at = timezone.now()
    waypoint.completed_at = completed_at
    waypoint.save()

    route = Route.objects.get(id = waypoint.route_id)
    # If all waypoints are completed, complete the route.
    if route.waypoints.filter(completed_at__isnull = True).count() == 0:
        route.completed_at = completed_at
        route.save()

    return JsonResponse({"status": "success"})

@csrf_exempt
# POST - params: access_token, route_id
def driver_start_route(request):
    # Get token
    access_token = AccessToken.objects.get(token = request.POST.get("access_token"),
        expires__gt = timezone.now())

    # Get driver
    driver = access_token.user.driver

    # Get waypoint
    route = Route.objects.get(id = request.POST["route_id"])

    if route.started_at is not None:
        return JsonResponse({"status": "failed", "error": "route already started."})

    # start route
    started_at = timezone.now()
    route.started_at = started_at
    route.save()

    return JsonResponse({"status": "success"})
