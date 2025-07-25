from django.contrib import admin
from .models import Room, Reservation
# Register your models here.


from .models import Room, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'capacity', 'price']

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'room']
    actions = ['confirm_reservations', 'cancel_reservations']

    @admin.action(description="Підтвердити обрані бронювання")
    def confirm_reservations(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description="Скасувати обрані бронювання")
    def cancel_reservations(self, request, queryset):
        queryset.update(status='cancelled')
