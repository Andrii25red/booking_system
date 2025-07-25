
from django.shortcuts import render, redirect
from .models import Room, Reservation
from .forms import ReservationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q

def availability_view(request):
    rooms = Room.objects.all()
    selected_room_id = request.GET.get('room')
    selected_room = None
    reservations = []

    if selected_room_id:
        selected_room = Room.objects.get(id=selected_room_id)
        reservations = Reservation.objects.filter(room=selected_room).order_by('start_date')

    return render(request,'availability.html', {
        'rooms': rooms,
        'selected_room': selected_room,
        'reservations': reservations
    })

def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})

@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.save()

            # Надсилання email підтвердження
            send_mail(
                subject="Підтвердження бронювання",
                message=f"Ваше бронювання підтверджено: {reservation.room} з {reservation.start_date} до {reservation.end_date}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[request.user.email],
                fail_silently=True,
            )

            return redirect('home')
    else:
        form = ReservationForm()
    return render(request, 'make_reservation.html', {'form': form})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'my_reservations.html', {'reservations': reservations})

