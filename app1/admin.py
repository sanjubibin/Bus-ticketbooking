from django.contrib import admin
from .models import Places, Bus, UserBooking, BusStatus
from .forms import PlaceForm, BusForm, UserBookingForm, BusStatusForm



class PlaceAdmin(admin.ModelAdmin):
    form = PlaceForm
    list_display = ["id", "places"]
    sortable_by = ["id"]

class BusAdmin(admin.ModelAdmin):
    form = BusForm
    list_display = ["id","bus_no", "bus_name", "total_seats", "bus_type"]
    sortable_by = ["id"]

admin.site.register(Places, PlaceAdmin)
admin.site.register(Bus, BusAdmin)
admin.site.register(UserBooking)
admin.site.register(BusStatus)

