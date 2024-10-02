"""
URL configuration for edan_homestay project.

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
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('user_login/', views.user_login, name='user_login'),
    path('registration/', views.registration, name='registration'),
    path('edan_room/', views.edan_room, name='edan_room'),
    path('guest_registration/', views.guest_registration, name='guest_registration'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_manage_room/', views.admin_manage_room, name='admin_manage_room'),
    path('admin_add_room/', views.admin_add_room, name='admin_add_room'),
    path('admin_edit_room/<int:room_id>/', views.admin_edit_room, name='admin_edit_room'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('admin_manage_bookings/', views.admin_manage_bookings, name='admin_manage_bookings'),
    path('admin_manage_bookings/<int:booking_id>/', views.admin_view_booking, name='admin_view_booking'),
    path('admin_send_message/<int:booking_id>/', views.admin_send_message, name='admin_send_message'),
    path('admin_manage_payment/', views.admin_manage_payment, name='admin_manage_payment'),
    path('admin_manage_guest/', views.admin_manage_guest, name='admin_manage_guest'),
    path('admin_view_guest_details/<int:guest_id>/', views.admin_view_guest_details, name='admin_view_guest_details'),
    path('admin_add_guest/', views.admin_add_guest, name='admin_add_guest'),
    path('delete_guest/<int:id>/', views.delete_guest, name='delete_guest'),
    path('guest_home/', views.guest_home, name='guest_home'),
    path('guest_room/', views.guest_room, name='guest_room'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('edan_room_detail/<int:room_id>/', views.edan_room_detail, name='edan_room_detail'),
    path('guest_booking/', views.guest_booking, name='guest_booking'),
    path('guest_profile/', views.guest_profile, name='guest_profile'),
    path('edit_guest_profile/', views.edit_guest_profile, name='edit_guest_profile'),
    path('admin_profile/', views.admin_profile, name='admin_profile'),
    path('book/<int:room_id>/', views.guest_book_room, name='guest_book_room'),
    path('payment/<int:booking_id>/<advance_payment>/', views.payment_page, name='payment_page'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('refund-request/<int:booking_id>/', views.refund_request, name='refund_request'),
]
