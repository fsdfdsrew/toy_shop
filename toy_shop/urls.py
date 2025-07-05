"""
URL configuration for toy_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from toys.views import home, toy_detail, shop, cart_detail, cart_add, cart_remove, cart_clear, cart_decrease, checkout, order_success

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),  # URL для смены языка
    path('', home, name='home'),  # добавьте этот маршрут
    path('shop/', shop, name='shop'),
    path('toys/<slug:slug>/', toy_detail, name='toy_detail'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/add/<int:toy_id>/', cart_add, name='cart_add'),
    path('cart/remove/<int:toy_id>/', cart_remove, name='cart_remove'),
    path('cart/decrease/<int:toy_id>/', cart_decrease, name='cart_decrease'),
    path('cart/clear/', cart_clear, name='cart_clear'),
    path('checkout/', checkout, name='checkout'),
    path('order/success/<str:order_number>/', order_success, name='order_success'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)