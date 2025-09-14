from django.contrib import admin
from .models import ParkingSlot, ParkingRecord

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'floor', 'status', 'vehicle_type', 'updated_at')
    list_filter = ('status', 'floor', 'vehicle_type')
    search_fields = ('slot_number',)

@admin.register(ParkingRecord)
class ParkingRecordAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'parking_slot', 'driver_name', 'check_in_time', 'check_out_time', 'fee_charged')
    list_filter = ('check_in_time', 'check_out_time')
    search_fields = ('vehicle_number', 'driver_name')
