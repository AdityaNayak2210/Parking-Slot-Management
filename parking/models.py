from django.db import models
from django.contrib.auth.models import User

class ParkingSlot(models.Model):
    SLOT_STATUS = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Under Maintenance'),
    )
    
    slot_number = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField()
    status = models.CharField(max_length=20, choices=SLOT_STATUS, default='available')
    vehicle_type = models.CharField(max_length=20, default='car')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Slot {self.slot_number} - {self.status}"

class ParkingRecord(models.Model):
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    fee_charged = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    def __str__(self):
        return f"{self.vehicle_number} - {self.parking_slot.slot_number}"
