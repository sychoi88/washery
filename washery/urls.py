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
from washeryapp import views
from django.contrib.auth import views as auth_views

from django.conf.urls.static import static
from django.conf import settings

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

    # Sign In/ Sign Up/ Sign Out
    url(r'^api/social/', include('rest_framework_social_oauth2.urls')),
    # /convert-token (sign in/ sign up)
    # /revoke-token (sign out)


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
