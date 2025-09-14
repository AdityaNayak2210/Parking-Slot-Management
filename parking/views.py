from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count
from .models import ParkingSlot, ParkingRecord
from django.utils import timezone

def home(request):
    # Get statistics for dashboard
    total_slots = ParkingSlot.objects.count()
    available_slots = ParkingSlot.objects.filter(status='available').count()
    occupied_slots = ParkingSlot.objects.filter(status='occupied').count()
    total_records = ParkingRecord.objects.count()
    
    # Get recent parking records
    recent_records = ParkingRecord.objects.order_by('-check_in_time')[:5]
    
    context = {
        'total_slots': total_slots,
        'available_slots': available_slots,
        'occupied_slots': occupied_slots,
        'total_records': total_records,
        'recent_records': recent_records,
    }
    return render(request, 'parking/home.html', context)

def parking_slots(request):
    slots = ParkingSlot.objects.all().order_by('floor', 'slot_number')
    return render(request, 'parking/parking_slots.html', {'slots': slots})

def parking_records(request):
    records = ParkingRecord.objects.all().order_by('-check_in_time')
    return render(request, 'parking/parking_records.html', {'records': records})

def add_parking_record(request):
    if request.method == 'POST':
        slot_id = request.POST.get('parking_slot')
        slot = get_object_or_404(ParkingSlot, id=slot_id)
        
        if slot.status != 'available':
            messages.error(request, 'Selected parking slot is not available.')
            return redirect('add_parking_record')
        
        record = ParkingRecord(
            parking_slot=slot,
            vehicle_number=request.POST.get('vehicle_number'),
            driver_name=request.POST.get('driver_name'),
            driver_phone=request.POST.get('driver_phone')
        )
        record.save()
        
        # Update slot status
        slot.status = 'occupied'
        slot.save()
        
        messages.success(request, 'Parking record created successfully.')
        return redirect('parking_records')
    
    available_slots = ParkingSlot.objects.filter(status='available')
    return render(request, 'parking/add_parking_record.html', {'available_slots': available_slots})

def checkout_vehicle(request, record_id):
    record = get_object_or_404(ParkingRecord, id=record_id)
    
    if request.method == 'POST':
        record.check_out_time = timezone.now()
        record.fee_charged = calculate_parking_fee(record)
        record.save()
        
        # Update slot status
        slot = record.parking_slot
        slot.status = 'available'
        slot.save()
        
        messages.success(request, 'Vehicle checked out successfully.')
        return redirect('parking_records')
    
    return render(request, 'parking/checkout_vehicle.html', {'record': record})

def calculate_parking_fee(record):
    # Get duration
    duration = timezone.now() - record.check_in_time
    hours = duration.total_seconds() / 3600
    days = hours // 24
    remaining_hours = hours % 24

    # Get vehicle type from parking slot
    vehicle_type = record.parking_slot.vehicle_type.lower()

    # Set rates based on vehicle type
    if vehicle_type == 'bike':
        hourly_rate = 20  # INR 20 per hour for bikes
        daily_rate = 350  # INR 350 per day for bikes
    else:  # default to car rates
        hourly_rate = 30  # INR 30 per hour for cars
        daily_rate = 600  # INR 600 per day for cars

    # Calculate total fee
    total_fee = (days * daily_rate) + (min(remaining_hours, 24) * hourly_rate)
    
    # Round to 2 decimal places
    return round(total_fee, 2)
