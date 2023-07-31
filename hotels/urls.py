from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_page, name="login"),
    path('register', views.register_page, name="register"),
    path('hotel-detail/<uid>/', views.hotel_detail, name="hotel_detail"),
    path('logout', views.logout_page, name="logout"),
    path('limit', views.check_limit, name="check_limit"),
    path('check', views.user_booking, name="checkBooking"),
    path('contact', views.contact, name="contact"),
    path('profile', views.profile, name="profile"),
    path('delete/<str:id>', views.delete, name="delete"),




]
