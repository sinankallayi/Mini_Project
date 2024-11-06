from pyexpat.errors import messages
from django import forms
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from . models import *
from django.db import IntegrityError
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from decimal import Decimal
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.http import HttpResponse


# Create your views here.
def index(request):
    rooms = room_table.objects.all()  # Fetch all rooms
    room_reviews = []  # To store reviews for each room

    for room in rooms:
        ratings = Rating.objects.filter(room=room)  # Get ratings for the room
        feedbacks = Feedback.objects.filter(room=room)  # Get feedback for the room
        room_reviews.append({
            'room': room,
            'ratings': ratings,
            'feedbacks': feedbacks,
        })

    return render(request, 'edan/index.html', {'room_reviews': room_reviews})
    

def login(request):
    return render(request,'edan/login.html')


# def forgot_password(request):
#     return render(request, 'edan/forgot_password.html')



# def forgot_password(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             user = User.objects.get(email=email)
#             # Generate token and send email (implement email sending logic)
#             token = default_token_generator.make_token(user)
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             # Construct your reset link here
#             reset_link = f"{request.scheme}://{request.get_host()}/reset-password/{uid}/{token}/"
#             send_mail(
#                 'Password Reset Request',
#                 f'Click the link to reset your password: {reset_link}',
#                 'your_email@example.com',
#                 [user.email],
#             )
#             return render(request, 'forgot_password.html', {'success_message': 'Reset link sent to your email.'})
#         except User.DoesNotExist:
#             return render(request, 'forgot_password.html', {'error_message': 'Email not found.'})
#     return render(request, 'edan/forgot_password.html')


def registration(request):
    return render(request,'edan/guest_registration.html')

def list_rooms(request):
    return render(request,'edan/list_rooms.html')

def admin_dashboard(request):
    total_rooms = room_table.objects.count()  # Count of total rooms
    total_bookings = booking_table.objects.count()  # Count of total bookings
    total_guests= guest_table.objects.count()
    total_revenue = Payment.objects.filter(status='Completed').aggregate(Sum('amount'))['amount__sum'] or 0
    ratings = Rating.objects.all().order_by('-id')  # Fetch all ratings
    feedbacks = Feedback.objects.all().order_by('-id')  # Fetch all feedbacks

    context = {
        'total_rooms': total_rooms,
        'total_bookings': total_bookings,
        'total_guests': total_guests,
        'total_revenue': total_revenue,
        'ratings': ratings,
        'feedbacks': feedbacks,

    }
    return render(request,'admin/admin_dashboard.html',context)

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

def edan_view_payment_details(request, payment_id):
    payment = get_object_or_404(Payment, pk=payment_id)
    return render(request, 'admin/admin_payment_details.html', {'payment': payment})


def admin_manage_guest(request):
    data_set = guest_table.objects.all().order_by('-id')
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
    rooms = room_table.objects.all()  # Fetch all rooms
    room_reviews = []  # To store reviews for each room

    for room in rooms:
        ratings = Rating.objects.filter(room=room)  # Get ratings for the room
        feedbacks = Feedback.objects.filter(room=room)  # Get feedback for the room
        room_reviews.append({
            'room': room,
            'ratings': ratings,
            'feedbacks': feedbacks,
        })

    return render(request, 'guest/guest_home.html', {'room_reviews': room_reviews})


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

        # Calculate the total stay amount based on days
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d')
        total_days = (check_out_date - check_in_date).days
        
        # Calculate total amount based on the total number of days and room price
        total_amount = room.price * total_days

        # Ensure advance payment does not exceed total amount
        if advance_payment > total_amount:
            return render(request, 'guest/guest_booking_room.html', {
                'room': room,
                'half_price': half_price,
                'error_message': 'Advance payment cannot exceed the total amount.',
                'total_amount': total_amount,
            })

        # Calculate the balance amount correctly
        balance_amount = total_amount - advance_payment

        # Create a booking entry with 'Pending' status
        booking = booking_table(
            guest=guest,
            room=room,
            check_in=check_in,
            check_out=check_out,
            number_of_guests=number_of_guests,
            advance_payment=advance_payment,
            balance_amount=balance_amount,  # Save the correct balance amount
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

        # Simulate payment processing
        advance_payment = Decimal(advance_payment)

        # Update booking details
        booking.balance_amount = booking.balance_amount  # Keep the original balance amount from the booking entry
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



def guest_booking(request):
    guest_id = request.session.get('lid')
    if not guest_id:
        return redirect('/login')

    try:
        guest = guest_table.objects.get(login_id=guest_id)
        bookings = booking_table.objects.filter(guest=guest)
        messages_for_guest = Message.objects.filter(guest=guest)
    except guest_table.DoesNotExist:
        return redirect('/login')

    return render(request, 'guest/guest_booking.html', {
        'guest': guest,
        'bookings': bookings,
        'messages_for_guest': messages_for_guest,
    })



def guest_notifications(request):
    guest_id = request.session.get('lid')
    if not guest_id:
        return redirect('/login')

    try:
        guest = guest_table.objects.get(login_id=guest_id)
        messages_for_guest = Message.objects.filter(guest=guest).order_by('-sent_at')  # Latest messages first
    except guest_table.DoesNotExist:
        return redirect('/login')

    return render(request, 'guest/guest_notifications.html', {
        'guest': guest,
        'messages_for_guest': messages_for_guest,
    })



# def notifications_view(request):
#     # Get all messages for the logged-in guest
#     messages_for_guest = Message.objects.filter(guest=request.user)

#     # Count unread messages
#     unread_count = messages_for_guest.filter(is_read=False).count()

#     # Pass messages and unread count to the template
#     context = {
#         'messages_for_guest': messages_for_guest,
#         'unread_count': unread_count,
#     }
#     return render(request, 'guest/guest_notifications.html', context)




def cancel_booking(request, booking_id):
    if request.method == 'POST':
        # Retrieve the booking record
        booking = get_object_or_404(booking_table, booking_id=booking_id)

        # Update booking status to 'Cancelled'
        booking.status = 'Cancelled'
        booking.save()

        # Redirect to the guest bookings page
        return redirect('guest_booking')

    # If not a POST request, redirect back to the bookings page
    return redirect('guest_booking')







# def refund_request_form(request, booking_id):
#     booking = get_object_or_404(booking_table, booking_id=booking_id)

#     if request.method == 'POST':
#         # Collect form data
#         first_name = request.POST.get('firstName')
#         email = request.POST.get('email')
#         account_number = request.POST.get('accountNumber')
#         ifsc_code = request.POST.get('ifsc')

#         # Validate booking status
#         if booking.status == 'Cancelled':
#             # Check cancellation policy (refund if canceled 7+ days before check-in)
#             check_in_datetime = datetime.combine(booking.check_in, datetime.min.time())
#             if timezone.make_aware(check_in_datetime) > timezone.now() + timedelta(days=7):
#                 booking.status = 'Refund Requested'
#                 booking.save()

#                 # Update payment status
#                 payment = Payment.objects.filter(booking=booking).first()
#                 if payment:
#                     payment.status = 'Refund Requested'
#                     payment.save()

#                 # Save refund information
#                 Refund.objects.create(
#                     booking=booking,
#                     amount_refunded=booking.advance_payment,
#                     reason='Refund requested via form.',
#                     account_number=account_number,
#                     ifsc=ifsc_code
#                 )

#                 messages.success(request, 'Your refund request has been submitted successfully.')
#                 return redirect('guest_booking')
#             else:
#                 messages.error(request, 'Refund not allowed as per the cancellation policy.')
#         else:
#             messages.error(request, 'Refund request is only allowed for cancelled bookings.')

#     return render(request, 'guest/guest_refund_request_form.html', {'booking': booking})



def rate_room(request, room_id):
    room = get_object_or_404(room_table, id=room_id)  # Get the selected room

    guest_id = request.session.get('lid')  # Assuming guest session ID is stored in 'lid'
    guest = get_object_or_404(guest_table, login_id=guest_id)  # Fetch the guest

    if request.method == 'POST':
        rating_value = request.POST.get('rating')  # Get the rating value
        feedback_text = request.POST.get('feedback')  # Get feedback text

        # Create and save Rating object
        Rating.objects.create(guest=guest, room=room, rating=rating_value)

        # Create and save Feedback object
        Feedback.objects.create(guest=guest, room=room, feedback=feedback_text)

        return redirect('guest_booking')  # Redirect after submission

    return render(request, 'guest/rate_room.html', {'room': room})


def refund_request_view(request, booking_id):
    booking = get_object_or_404(booking_table, booking_id=booking_id)

    if request.method == 'POST':
        # Retrieve and validate form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        account_number = request.POST.get('account_number')
        ifsc_code = request.POST.get('ifsc_code')

        # Debug: Print form data
        print(f"Name: {name}, Email: {email}, Account: {account_number}, IFSC: {ifsc_code}")

        # Check if the refund request is eligible
        current_date = now().date()
        cancellation_limit = booking.check_in - timedelta(days=7)

        if booking.status == 'Cancelled' and current_date < cancellation_limit:
            # Save the refund request
            refund_request = RefundRequest(
                booking=booking,
                name=name,
                email=email,
                account_number=account_number,
                ifsc_code=ifsc_code
            )
            refund_request.save()

            # Update booking status
            booking.status = 'Refund Requested'
            booking.save()

            messages.success(request, 'Refund request submitted successfully.')
            return redirect('guest_booking')
        else:
            messages.error(request, 'Refund not allowed as per cancellation policy.')

    return render(request, 'guest/guest_refund_request_form.html', {'booking': booking})



def edan_terms_policy(request):
    return render(request, 'edan/edan_terms_and_policy.html')



def process_refund(request, refund_id):
    refund_request = get_object_or_404(RefundRequest, id=refund_id)
    booking = refund_request.booking

    # Calculate refund amount (assuming it's the advance payment or any other logic you prefer)
    refund_amount = booking.advance_payment

    if request.method == "POST":
        # Create a refund record
        refund = Refund.objects.create(
            booking=booking,
            amount_refunded=refund_amount
        )

        # Update the booking and payment statuses
        booking.status = "Refunded"
        booking.save()

        # Update payment status for this booking
        payment = Payment.objects.filter(booking=booking).first()
        if payment:
            payment.status = "Refunded"
            payment.save()

        # Display a success message and redirect to a relevant page
        messages.success(request, "Refund processed successfully!")
        return redirect("admin_manage_payment")  # Update with your desired redirect page

    return render(request, "admin/process_refund.html", {
        "refund_request": refund_request,
        "refund_amount": refund_amount,
    })
