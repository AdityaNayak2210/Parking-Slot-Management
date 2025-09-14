# Parking Management System

A Django-based parking management system that helps manage parking slots and vehicle records efficiently.

## Project Structure

```
parking_management/
├── parking/                 # Main application directory
│   ├── models.py           # Database models
│   ├── admin.py           # Admin interface configuration
│   └── migrations/        # Database migrations
├── parking_management/     # Project settings directory
│   ├── settings.py        # Project settings
│   └── urls.py           # URL configurations
├── manage.py              # Django management script
├── requirements.txt       # Project dependencies
└── venv/                 # Virtual environment
```

## Features

### 1. Parking Slot Management
- Each parking slot has:
  - Unique slot number
  - Floor number
  - Current status (available/occupied/reserved/maintenance)
  - Vehicle type specification
  - Timestamp tracking (created/updated)

### 2. Parking Record System
- Tracks vehicle parking details:
  - Vehicle number
  - Driver information (name and phone)
  - Check-in and check-out times
  - Associated parking slot
  - Parking fee calculation

## Setup Instructions

1. Create and activate virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   source venv/bin/activate # Linux/Mac
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

4. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run development server:
   ```bash
   python manage.py runserver
   ```

## Database Models

### ParkingSlot Model
```python
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
```

### ParkingRecord Model
```python
class ParkingRecord(models.Model):
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    driver_name = models.CharField(max_length=100)
    driver_phone = models.CharField(max_length=15)
    check_in_time = models.DateTimeField(auto_now_add=True)
    check_out_time = models.DateTimeField(null=True, blank=True)
    fee_charged = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
```

## Usage Guide

### 1. Admin Interface
1. Access admin panel at: `http://127.0.0.1:8000/admin`
2. Login with superuser credentials

### 2. Managing Parking Slots
1. Go to "Parking slots" in admin panel
2. Add new parking slots with:
   - Slot number
   - Floor number
   - Initial status
   - Vehicle type

### 3. Recording Parking Transactions
1. Go to "Parking records" in admin panel
2. Create new record with:
   - Select parking slot
   - Enter vehicle details
   - Enter driver information
   - Check-in time is auto-recorded
   - Update check-out time when vehicle leaves
   - Enter parking fee charged

## Working Flow

1. **Slot Creation**
   - Admin creates parking slots
   - Assigns floor numbers
   - Sets initial status as 'available'

2. **Vehicle Check-in**
   - Staff selects available parking slot
   - Creates parking record with vehicle details
   - Slot status automatically changes to 'occupied'
   - Check-in time is recorded

3. **Vehicle Check-out**
   - Staff updates parking record
   - Enters check-out time
   - Records parking fee
   - Slot status returns to 'available'

4. **Monitoring**
   - Admin can view all current and past parking records
   - Track slot availability
   - Monitor parking duration
   - Review parking fees

## Security Features
- Django admin authentication
- User session management
- CSRF protection
- Secure password handling

## Data Management
- All records are stored in SQLite database
- Automatic timestamp tracking
- Relationship mapping between slots and records
- Unique constraints on slot numbers

## Future Enhancements Possible
1. Automated fee calculation based on duration
2. Mobile app integration
3. Payment gateway integration
4. QR code based check-in/check-out
5. Real-time slot availability dashboard
6. Customer notification system
7. Monthly/yearly parking pass management 