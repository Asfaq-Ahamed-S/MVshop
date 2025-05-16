from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


app_name = 'Shop'

# HTTP
'''
urlpatterns = [
    path('',views.index,name="index"),
    path('cart/<int:cart_id>',views.cart,name="cart"),
    path('new_url_different_path',views.new_url_view,name="new_url"),
    path('old_url',views.old_url,name="old_url"),
]
'''

# HTML

urlpatterns = [
    path('',views.index,name="index"),
    path('cart',views.cart,name="cart"),
    path('<int:product_id>',views.detail,name='detail'),
    path('detail_category\<int:category_id>',views.detail_category,name='detail_category'),
    path('register',views.register,name="register"),
    path('admin_register',views.admin_register,name="admin_register"),
    path('login',views.user_login,name="login"),
    path('logout',views.user_logout,name="logout"),
    path('category',views.category,name="category"),
    path('about',views.about,name="about"),
    path('add_to_cart\<int:product_id>',views.add_to_cart,name='add_to_cart'),
    path('remove-from-cart\<int:item_id>',views.remove_from_cart,name='remove_from_cart'),
    path('checkout',views.checkout,name="checkout"),
    path('process-checkout',views.process_checkout,name="process_checkout"),
    path('my-orders',views.my_orders,name="my_orders"),
    path('cancel-order\<int:order_id>',views.cancel_order,name="cancel_order"),
    path('payment-success',views.payment_success,name="payment_success"),
    path('payment-cancelled',views.payment_cancelled,name="payment_cancelled"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)