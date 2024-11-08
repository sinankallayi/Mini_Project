from django.db import models
from django.utils.timezone import now
from datetime import timedelta, timezone

# Create your models here.
class LoginTable(models.Model):
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=20)

    def __str__(self):
        return self.email


class guest_table(models.Model):
    login = models.ForeignKey(LoginTable, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    number = models.BigIntegerField()
    email = models.CharField(max_length=100)
    image = models.ImageField(upload_to='guest_images/')
    aadhaar_image = models.ImageField(upload_to='aadhaar_images/', blank=True, null=True)  # Aadhaar image field

    def __str__(self):
        return self.name

    

    

class room_table(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.CharField(max_length=50)

class RoomImage(models.Model):
    room = models.ForeignKey(room_table, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')

class RoomVideo(models.Model):
    room = models.ForeignKey(room_table, related_name='videos', on_delete=models.CASCADE)
    video = models.FileField(upload_to='room_videos/')



class booking_table(models.Model):
    BOOKING_STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('CheckedIn', 'Checked In'),
        ('CheckedOut', 'Checked Out'),
        ('Cancelled', 'Cancelled'),
        ('RefundRequested', 'Refund Requested'),
        ('Refunded', 'Refunded'),
    ]

    booking_id = models.AutoField(primary_key=True)  # Auto-incrementing booking ID
    guest = models.ForeignKey(guest_table, on_delete=models.CASCADE)  # Guest foreign key
    room = models.ForeignKey(room_table, on_delete=models.CASCADE)  # Room foreign key
    check_in = models.DateField()  # Check-in date
    check_out = models.DateField()  # Check-out date
    number_of_guests = models.IntegerField()  # Number of guests
    advance_payment = models.DecimalField(max_digits=10, decimal_places=2)  # Advance payment amount
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Optional balance amount
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='Booked')  # Booking status

    def __str__(self):
        return f"Booking {self.booking_id} - {self.guest.name} ({self.room.name})"
    


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Credit Card', 'Credit Card'),
        ('Debit Card', 'Debit Card'),
        ('PayPal', 'PayPal'),
        # Add more payment methods as needed
    ]

    payment_id = models.AutoField(primary_key=True)  # Auto-incrementing payment ID
    booking = models.ForeignKey(booking_table, on_delete=models.CASCADE)  # Link to the booking
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount paid
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)  # Payment method
    payment_date = models.DateTimeField(auto_now_add=True)  # Timestamp of payment
    status = models.CharField(max_length=20, default='Pending')  # Payment status

    def __str__(self):
        return f"Payment {self.payment_id} for Booking {self.booking.booking_id} - Amount: ₹{self.amount}"
    


class Message(models.Model):
    guest = models.ForeignKey(guest_table, on_delete=models.CASCADE)  # Relationship to the guest
    booking = models.ForeignKey(booking_table, on_delete=models.CASCADE)  # Link to the booking
    content = models.TextField()  # The message content
    sent_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the message is sent
    # Optional fields (you can add these as needed)
    sent_by = models.CharField(max_length=100, default='admin')  # This can be 'admin' or 'guest'
    
    def __str__(self):
        return f"Message to {self.guest.name}"
    


class Rating(models.Model):
    guest = models.ForeignKey(guest_table, on_delete=models.CASCADE)  # Guest foreign key
    room = models.ForeignKey(room_table, on_delete=models.CASCADE)    # Room foreign key
    rating = models.IntegerField()  # Rating value (1-5 stars)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the rating was made

    def __str__(self):
        return f"{self.guest.name} rated {self.room.name} - {self.rating} stars"

class Feedback(models.Model):
    guest = models.ForeignKey(guest_table, on_delete=models.CASCADE)  # Guest foreign key
    room = models.ForeignKey(room_table, on_delete=models.CASCADE)    # Room foreign key
    feedback = models.TextField()  # Feedback text
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the feedback was submitted

    def __str__(self):
        return f"Feedback by {self.guest.name} for {self.room.name}"


class Refund(models.Model):
    refund_id = models.AutoField(primary_key=True)  # Auto-incrementing refund ID
    booking = models.ForeignKey('booking_table', on_delete=models.CASCADE)  # Link to booking
    amount_refunded = models.DecimalField(max_digits=10, decimal_places=2)  # Amount refunded
    refund_date = models.DateTimeField(auto_now_add=True)  # Timestamp of refund
    reason = models.TextField(blank=True, null=True)  # Optional: Reason for refund

    def __str__(self):
        return f"Refund {self.refund_id} for Booking {self.booking.booking_id} - ₹{self.amount_refunded}"


class RefundRequest(models.Model):
    booking = models.OneToOneField('booking_table', on_delete=models.CASCADE, null=True)  
    name = models.CharField(max_length=100)
    email = models.EmailField()
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund Request from {self.name} for Booking {self.booking.booking_id if self.booking else 'N/A'}"