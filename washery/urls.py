"""washery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from washeryapp import views, apis

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home, name='home'),

    # Cleaner
    url(r'^cleaner/sign-in/$', auth_views.login,
        {'template_name': 'cleaner/sign_in.html'},
        name = 'cleaner-sign-in'),
    url(r'^cleaner/sign-out/$', auth_views.logout,
        {'next_page': '/'},
        name = 'cleaner-sign-out'),
    url(r'^cleaner/sign-up/$', views.cleaner_sign_up,
        name = 'cleaner-sign-up'),
    url(r'^cleaner/$', views.cleaner_home, name = 'cleaner_home'),

    url(r'^cleaner/account/$', views.cleaner_account, name = 'cleaner-account'),
    url(r'^cleaner/item/$', views.cleaner_item, name = 'cleaner-item'),
    url(r'^cleaner/item/add/$', views.cleaner_add_item, name = 'cleaner-add-item'),
    url(r'^cleaner/item/edit/(?P<item_id>\d+)/$', views.cleaner_edit_item, name = 'cleaner-edit-item'),

    # INVOICE
    url(r'^cleaner/invoice/$', views.cleaner_invoice, name = 'cleaner-invoice'),
    # url(r'^cleaner/invoice/add/$', views.cleaner_add_invoice, name = 'cleaner-add-invoice'),
    url(r'^cleaner/invoice/edit/$', views.cleaner_edit_invoice, name = 'cleaner-add-invoice'),
    url(r'^cleaner/invoice/edit/(?P<invoice_id>\d+)/$', views.cleaner_edit_invoice, name = 'cleaner-edit-invoice'),
    url(r'^cleaner/report/$', views.cleaner_report, name = 'cleaner-report'),


    # # Route
    url(r'^cleaner/route/$', views.cleaner_route, name = 'cleaner-route'),
    # url(r'^cleaner/route/add/$', views.cleaner_add_route, name='cleaner-add-route'),    # view to add route
    url(r'^cleaner/route/add/$', views.cleaner_edit_route, name='cleaner-add-route'),    # view to add route
    url(r'^cleaner/route/edit/(?P<route_id>\d+)/$', views.cleaner_edit_route, name='cleaner-edit-route'),    # view to add route


    # # Invoice
    # url(r'^cleaner/invoice/$', views.cleaner_invoice, name = 'cleaner-invoice'),

    # Sign In/ Sign Up/ Sign Out
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)
    url(r'^api/cleaner/invoice/notification/(?P<last_request_time>.+)/$',apis.cleaner_invoice_notification),
    url(r'^api/cleaner/items/$',apis.cleaner_get_items),

    # APIs for CLEANERS
    url(r'^api/cleaner/invoice/update-new/$', apis.cleaner_update_invoice_new), # this is used by web. validates csrf.
    url(r'^api/cleaner/invoice/update/$', apis.cleaner_update_invoice), #this ignores csrf. dont think this is being used.

    url(r'^api/cleaner/invoiceToEdit/(?P<invoice_id>\d+)/$', apis.cleaner_invoiceToEdit), # GET INVOICE WITH POS_ITEMS

    url(r'^api/cleaner/routeToEdit/(?P<route_id>\d+)/$', apis.cleaner_routeToEdit), # GET ROUTE WITH OPTIONS
    url(r'^api/cleaner/route/update/$', apis.cleaner_update_route), # POST TO UPDATE ROUTE

    # APIs for CUSTOMERS
    url(r'^api/customer/cleaners/$', apis.customer_get_cleaners),
    url(r'^api/customer/items/(?P<cleaner_id>\d+)/$', apis.customer_get_items),
    url(r'^api/customer/invoice/add$', apis.customer_add_invoice),
    url(r'^api/customer/invoice/request/$', apis.customer_request_invoice),

    url(r'^api/customer/invoice/latest/$', apis.customer_get_latest_invoice),
    url(r'^api/customer/driver/location/$', apis.customer_driver_location),

    url(r'^api/customer/payment-method/update/$', apis.customer_payment_method_update),
    url(r'^api/customer/invoice/update-payment/$', apis.customer_update_payment),

    # APIs for DRIVERS
    url(r'^api/driver/invoices/ready/$', apis.driver_get_ready_invoices),
    url(r'^api/driver/invoice/pick/$', apis.driver_pick_invoice),
    url(r'^api/driver/invoice/latest/$', apis.driver_get_latest_invoice),
    url(r'^api/driver/invoice/complete/$', apis.driver_complete_invoice),
    url(r'^api/driver/revenue/$', apis.driver_get_revenue),
    url(r'^api/driver/location/update/$', apis.driver_update_location),

    # APIs for DRIVER ROUTES
    url(r'^api/driver/routes/$', apis.driver_get_routes),
    url(r'^api/driver/route/(?P<route_id>\d+)/$', apis.driver_get_route),

    url(r'^api/driver/route/latest/$', apis.driver_get_latest_route),
    url(r'^api/driver/waypoint/complete/$', apis.driver_complete_waypoint),
    url(r'^api/driver/route/start/$', apis.driver_start_route),

    # APIs for DRIVER WAYPOINTs
    url(r'^api/driver/waypoint/(?P<waypoint_id>\d+)/$', apis.driver_get_waypoint),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
