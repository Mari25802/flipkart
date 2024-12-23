from django.urls import path
from . import views

app_name='ekart'

urlpatterns=[
    path('',views.index, name="index"),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('logout_page', views.logout_page, name="logout_page"),
    path('cart', views.cart, name="cart"),
    path('remove_fav/<str:fid>', views.remove_fav, name="remove_fav"),
    path('remove_cart/<str:cid>', views.remove_cart, name="remove_cart"),
    path('cart_page', views.cart_page, name="cart_page"),
    path('fav', views.fav_page, name="fav_page"),
    path('fav_view', views.fav_view, name="fav_view"),
    path('collection', views.collection, name="collection"),
    path('collection/<str:name>', views.collectionview, name="collection"),
    path('collection/<str:cname>/<str:pname>', views.product_details, name="product_details")
]