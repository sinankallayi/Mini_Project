from pyexpat.errors import messages
from django import forms
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from . models import *
from . models import guest_table
from decimal import Decimal
from django.db import IntegrityError
from datetime import datetime
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request,'edan/index.html')

def login(request):
    return render(request,'edan/login.html')

def registration(request):
    return render(request,'edan/guest_registration.html')

def list_rooms(request):
    return render(request,'edan/list_rooms.html')

def admin_dashboard(request):
    return render(request,'admin/admin_dashboard.html')

def admin_manage_room(request):
    rooms = room_table.objects.all()
    return render(request,'admin/admin_manage_room.html',{'rooms':rooms})


def admin_add_room(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        type = request.POST.get('type')
        description = request.POST.get('description')
        price = request.POST.get('price')
        availability = request.POST.get('availability')  # lowercase value from form

        # Create a new room entry
        new_room = room_table(
            name=name,
            type=type,
            description=description,
            price=price,
            availability=availability  # Save as lowercase
        )
        new_room.save()

        # Handle multiple images
        images = request.FILES.getlist('images')
        for image in images:
            RoomImage.objects.create(room=new_room, image=image)

        # Handle multiple videos
        videos = request.FILES.getlist('videos')
        for video in videos:
            RoomVideo.objects.create(room=new_room, video=video)

        return redirect('admin_manage_room')

    return render(request, 'admin/admin_add_room.html')


def admin_edit_room(request, room_id):
    room = get_object_or_404(room_table, id=room_id)

    if request.method == 'POST':
        # Update the room details
        room.name = request.POST['name']
        room.type = request.POST['type']
        room.description = request.POST['description']
        room.price = request.POST['price']
        room.availability = request.POST['availability']  # Fix availability check
        room.save()

        # Handle new image uploads
        if request.FILES.getlist('images'):
            for image in request.FILES.getlist('images'):
                RoomImage.objects.create(room=room, image=image)

        # Handle new video uploads
        if request.FILES.getlist('videos'):
            for video in request.FILES.getlist('videos'):
                RoomVideo.objects.create(room=room, video=video)

        return redirect('admin_manage_room')

    context = {
        'room': room,
    }
    return render(request, 'admin/admin_edit_room.html', context)


def delete_room(request, room_id):
    room = room_table.objects.get(id=room_id)
    room.delete()
    return HttpResponse('''<script>alert("Room Deleted Successfully"); window.location="/admin_manage_room";</script>''')
    
    # if request.method == 'POST':
    #     room.delete()
    #     messages.success(request, "Room deleted successfully.")
    #     return redirect('manage_rooms')  # Redirect to the room management page after deletion

    # return render(request, 'confirm_delete.html', {'room': room})

# def admin_add_room(request):
#     if request.method == 'POST':
#         form = RoomForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('manage_rooms')  # Redirect to the same page after submission
#     else:
#         form = RoomForm()
    
#     rooms = Room.objects.all()
#     return render(request, 'manage_rooms.html', {'form': form, 'rooms': rooms})


def admin_manage_bookings(request):
    bookings = booking_table.objects.all().order_by('-booking_id')  # Sort by creation date in descending order
    return render(request, 'admin/admin_manage_bookings.html', {'bookings': bookings})


def admin_view_booking(request, booking_id):
    # Fetch the booking using the booking_id
    booking = get_object_or_404(booking_table, booking_id=booking_id)
    
    # Pass the booking to the template
    return render(request, 'admin/admin_view_booking.html', {'booking': booking})


# def admin_send_message(request, booking_id):
#     # Fetch the booking using the booking_id
#     booking = get_object_or_404(booking_table, booking_id=booking_id)

#     # Extract relevant data
#     guest_name = booking.guest.name
#     advance_payment = booking.advance_payment
#     balance_amount = booking.balance_amount
    
#     # Create your message content
#     message_content = f"Dear {guest_name}, your room booking is successful! " \
#                       f"Advance Amount: ₹{advance_payment}, Balance Amount: ₹{balance_amount}. " \
#                       "Welcome to Edan Homestay, and enjoy your stay!"
    
#     # Save the message in the Message model
#     Message.objects.create(
#         guest=booking.guest,
#         content=message_content,
#         booking=booking
#     )
    
#     # Display success message to the admin
#     messages.success(request, "Message sent successfully to the guest.")
    
#     return redirect('admin_view_booking', booking_id=booking_id)


def admin_send_message(request, booking_id):
    # Fetch the booking using the booking_id
    booking = get_object_or_404(booking_table, booking_id=booking_id)

    if request.method == "POST":
        # Get the custom message from the form
        custom_message = request.POST.get('messageContent')

        # Save the message in the Message model
        Message.objects.create(
            guest=booking.guest,
            content=custom_message,
            booking=booking
        )

        # Display success message to the admin
        messages.success(request, "Message sent successfully to the guest.")
    
    return redirect('admin_view_booking', booking_id=booking_id)




def admin_manage_payment(request):
    payments = Payment.objects.all().order_by('-payment_id')  # Retrieve all payment records from the database
    return render(request, 'admin/admin_manage_payment.html', {'payments': payments})


def admin_manage_guest(request):
    data_set = guest_table.objects.all()
    return render(request, 'admin/admin_manage_guest.html', {'guest': data_set})


def admin_view_guest_details(request, guest_id):
    guest = get_object_or_404(guest_table, id=guest_id)
    return render(request, 'admin/admin_view_guest_details.html', {'guest': guest})



def admin_add_guest(request):
    if request.method == "POST":
        name = request.POST['name']
        number = request.POST['number']
        email = request.POST['email']
        password = request.POST["password"]
        image = request.FILES.get('image')

        # Create a new login entry
        login_obj = LoginTable(email=email, password=password, role="guest")
        login_obj.save()

        # Create a new guest entry
        guest_obj = guest_table(name=name, number=number, email=email, image=image, login=login_obj)
        guest_obj.save()

        return redirect('admin_manage_guest')

    return render(request, 'admin/admin_add_guest.html')


def delete_guest(request, id):
    guest = guest_table.objects.get(id=id)
    guest.delete()
    return HttpResponse('''<script>alert("Guest Deleted Successfully"); window.location="/admin_manage_guest";</script>''')

def guest_home(request):
    return render(request,'guest/guest_home.html')

def guest_room(request):
    rooms = room_table.objects.all()  # Fetch all rooms
    return render(request, 'guest/guest_room.html', {'rooms': rooms})

def edan_room(request):
    # Fetch all rooms from the database
    rooms = room_table.objects.all()

    # Pass the rooms and the user's authentication status to the template
    return render(request, 'edan/list_rooms.html', {
        'rooms': rooms,
        'user': request.user  # To check if the user is authenticated in the template
    })

def guest_booking(request):
    guest_id = request.session.get('lid')
    if not guest_id:  # Check if guest_id is None or empty
        return redirect('/login')

    try:
        guest = guest_table.objects.get(login_id=guest_id)
        bookings = booking_table.objects.filter(guest=guest)
        # Retrieve messages for the guest
        messages_for_guest = Message.objects.filter(guest=guest)
    except guest_table.DoesNotExist:
        return redirect('/login')  # Or display an error message

    return render(request, 'guest/guest_booking.html', {
        'guest': guest,
        'bookings': bookings,
        'messages': messages_for_guest,  # Pass messages to the template
    })


def user_login(request):
    error_message = None  # Initialize error message as None
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        login_fetch = LoginTable.objects.filter(email=email, password=password)
        if login_fetch.exists():
            login_objects = LoginTable.objects.get(email=email, password=password)
            request.session['lid'] = login_objects.id

            # Redirect based on the user's role
            if login_objects.role == 'admin':
                return redirect('/admin_dashboard')  # Redirect to admin dashboard
            elif login_objects.role == 'guest':
                return redirect('/guest_home')  # Redirect to guest home
        else:
            # Set error message for invalid credentials
            error_message = "Invalid email or password."

    # Render login page with error message (if any)
    return render(request, 'edan/login.html', {'error_message': error_message}) 


def guest_registration(request):
    if request.method == 'POST':
        name = request.POST['name']
        number = request.POST['number']
        email = request.POST['email']
        password = request.POST['password']
        image = request.FILES.get('image')
        aadhaar_image = request.FILES.get('aadhaar_image')  # Capture Aadhaar image

        try:
            # Check for duplicate email and save data if email is unique
            login_obj = LoginTable(email=email, password=password, role="guest")
            login_obj.save()

            guest_obj = guest_table(name=name, number=number, email=email, image=image, aadhaar_image=aadhaar_image, login=login_obj)
            guest_obj.save()

            return HttpResponse('''<script>alert("Registration Successfully Completed"); window.location="/";</script>''')

        except IntegrityError:
            # If the email already exists, return the form with an error message
            error_message = "This email is already registered."
            return render(request, 'edan/guest_registration.html', {'error_message': error_message})

    return render(request, 'edan/login.html')


def guest_profile(request):
    # Get the logged-in user's login ID from the session
    login_id = request.session.get('lid')

    # Fetch the guest details based on the login ID
    guest_details = get_object_or_404(guest_table, login_id=login_id)

    # Render the guest profile page with the guest's details
    return render(request, 'guest/guest_profile.html', {'guest': guest_details})


def edit_guest_profile(request):
    login_id = request.session.get('lid')
    guest = get_object_or_404(guest_table, login_id=login_id)

    if request.method == 'POST':
        guest.name = request.POST['name']
        guest.number = request.POST['number']
        guest.email = request.POST['email']
        
        # Handle image update if a new image is uploaded
        if 'image' in request.FILES:
            guest.image = request.FILES['image']

        guest.save()
        return redirect('guest_profile')

    return render(request, 'guest/edit_guest_profile.html', {'guest': guest})


def room_detail(request, room_id):
    room = get_object_or_404(room_table, id=room_id)
    return render(request, 'guest/room_detail.html', {'room': room})

def edan_room_detail(request, room_id):
    room = get_object_or_404(room_table, id=room_id)
    return render(request, 'edan/edan_room_detail.html', {'room': room})

# def edan_room_list(request):
#     rooms = room_table.objects.all()  # Fetch all rooms from the database
#     return render(request, 'room_list.html', {'rooms': rooms})

# # View for individual room details
# def edan_room_detail(request, room_id):
#     room = get_object_or_404(room_table, id=room_id)  # Fetch room by its id
#     images = room.images.all()  # Assuming each room has a related set of images
#     return render(request, 'room_detail.html', {'room': room, 'images': images})



def admin_profile(request):
    # You can retrieve admin details from the database if needed. Here we assume hardcoded details for simplicity.
    admin_details = {
        'name': 'RISHAD ALI',
        'property_name': 'Edan Homestay',
        'contact_number': '+91 9876543210',
        'location': 'Pukayoor, Malappuram'
    }
    return render(request, 'admin/admin_profile.html', admin_details)



def guest_book_room(request, room_id):
    room = get_object_or_404(room_table, id=room_id)  # Get the selected room
    half_price = room.price / 2  # Calculate half price

    if request.method == 'POST':
        guest_id = request.session.get('lid')  # Assuming guest session ID is stored in 'lid'
        guest = get_object_or_404(guest_table, login_id=guest_id)  # Fetch the guest

        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        number_of_guests = request.POST.get('number_of_guests')
        advance_payment = Decimal(request.POST.get('advance_payment'))  # Convert to Decimal

        # Create a booking entry
        booking = booking_table(
            guest=guest,
            room=room,
            check_in=check_in,
            check_out=check_out,
            number_of_guests=number_of_guests,
            advance_payment=advance_payment,
            balance_amount=room.price - advance_payment,  # Calculate the balance
            status='Pending'
        )
        booking.save()

        # Redirect to the payment page
        return redirect('payment_page', booking_id=booking.booking_id, advance_payment=advance_payment)

    return render(request, 'guest/guest_booking_room.html', {'room': room, 'half_price': half_price})


def payment_page(request, booking_id, advance_payment):
    booking = get_object_or_404(booking_table, booking_id=booking_id)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        card_number = request.POST.get('card_number')
        card_expiry = request.POST.get('card_expiry')
        card_cvc = request.POST.get('card_cvc')

        # Here you would integrate with a payment gateway to process the payment.
        # For example, using Stripe, you would create a charge with the card details.

        # Simulate payment processing:
        # If payment is successful
        advance_payment = Decimal(advance_payment)

        # Update booking details
        booking.advance_payment = advance_payment
        booking.balance_amount = booking.room.price - advance_payment
        booking.status = 'Booked'
        booking.save()

        # Save payment information
        payment = Payment(
            booking=booking,
            amount=advance_payment,
            payment_method=payment_method,
            status='Completed'
        )
        payment.save()

        # Redirect after payment
        return redirect('guest_home')

    return render(request, 'guest/payment_page.html', {
        'booking_id': booking_id,
        'advance_payment': advance_payment
    })

# def booked_room_list(request):
#     guest_id = request.session.get('lid')
#     if not guest_id:  # Check if guest_id is None or empty
#         return redirect('/login')

#     try:
#         guest = guest_table.objects.get(login_id=guest_id)
#         bookings = booking_table.objects.filter(guest=guest)
#     except guest_table.DoesNotExist:
#         # Handle the case where the guest doesn't exist (maybe session data is corrupted)
#         return redirect('/login')  # Or display an error message

#     return render(request, 'guest/guest_booking.html', {
#         'guest': guest,
#         'bookings': bookings
#     })



def cancel_booking(request, booking_id):
    booking = get_object_or_404(booking_table, booking_id=booking_id)

    if request.method == 'POST' and booking.status != 'Cancelled':
        booking.status = 'Cancelled'
        booking.save()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def refund_request(request, booking_id):
    booking = get_object_or_404(booking_table, booking_id=booking_id)

    if request.method == 'POST' and booking.status == 'Cancelled':
        # Check the cancellation policy logic
        # Here you can implement any rules (e.g., time-based restrictions) if needed
        # For now, we just simulate a refund request confirmation
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# def search_results(request):
#     room_type = request.GET.get('room_type')
#     check_in = request.GET.get('check_in')
#     check_out = request.GET.get('check_out')
#     guests = request.GET.get('guests')

#     # Filter rooms based on the search criteria
#     rooms = room_table.objects.filter(
#         type__icontains=room_type,
#         availability='available'
#     )

#     context = {
#         'rooms': rooms,
#         'room_type': room_type,
#         'check_in': check_in,
#         'check_out': check_out,
#         'guests': guests,
#     }

#     return render(request, 'edan/list_rooms.html', context)
