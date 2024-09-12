from pyexpat.errors import messages
from django import forms
from django.shortcuts import redirect, render, HttpResponse, get_object_or_404
from . models import *
from . models import guest_table

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
        availability = request.POST.get('availability')

        # Create a new room entry
        new_room = room_table(
            name=name,
            type=type,
            description=description,
            price=price,
            availability=availability
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
    room = get_object_or_404(room_table, id=room_id)  # Correct model name

    if request.method == 'POST':
        # Update the room details
        room.name = request.POST['name']
        room.type = request.POST['type']
        room.description = request.POST['description']
        room.price = request.POST['price']
        room.availability = request.POST['availability']
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
    return render(request,'admin/admin_manage_bookings.html')

def admin_manage_payment(request):
    return render(request,'admin/admin_manage_payment.html')

def admin_manage_guest(request):
    data_set = guest_table.objects.all()
    return render(request, 'admin/admin_manage_guest.html', {'guest': data_set})

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
    return render(request,'guest/guest_room.html')

def guest_booking(request):
    return render(request,'guest/guest_booking.html')

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
        name = request.POST['name']
        number = request.POST['number']
        email = request.POST['email']
        image = request.FILES['image']
        password = request.POST["password"]


        login_obj=LoginTable(email=email,password=password,role="guest")
        login_obj.save()


        guest_obj=guest_table(name=name,number=number,email=email,image=image,login=login_obj)
        guest_obj.save()
        return HttpResponse('''<script>alert("Registration Successfully Completed"); window.location="/";</script>''')
