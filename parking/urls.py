from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('slots/', views.parking_slots, name='parking_slots'),
    path('records/', views.parking_records, name='parking_records'),
    path('records/add/', views.add_parking_record, name='add_parking_record'),
    path('records/checkout/<int:record_id>/', views.checkout_vehicle, name='checkout_vehicle'),
] 