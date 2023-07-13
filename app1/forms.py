from django import forms
from django.utils import timezone
from .models import Places, UserBooking, Bus, BusStatus
from django.contrib.auth.models import User

class ProfileForm(forms.Form):
    user_image = forms.ImageField(required=True, label="Profile Photo")
    address = forms.CharField(required=True)
    mobile = forms.CharField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

class SignInForm(forms.Form):
    username = forms.CharField(max_length=50, required=True, label="Your Name")
    email = forms.EmailField(required=True, label="Email:")
    password1 = forms.CharField(widget=forms.PasswordInput, required=True, label="Password:")
    password2 = forms.CharField(widget=forms.PasswordInput, required=True, label="Retype Password:")

class PlaceForm(forms.ModelForm):
    places = forms.CharField()

    class Meta:
        model = Places
        fields = ['places']

class BusForm(forms.ModelForm):
    BUS_TYPE_CHOICES = [
        ('sleeper', 'Sleeper'),
        ('ac_sleeper', 'AC Sleeper'),
        ('seated', 'Seated'),
        ('ac_seated', 'AC Seated'),
    ]

    bus_type = forms.ChoiceField(choices=BUS_TYPE_CHOICES)
    total_seats = forms.IntegerField(min_value=20, max_value=60)

    class Meta:
        model = Bus
        fields = ['bus_no', 'bus_name', 'total_seats', 'bus_type']


class BusStatusForm(forms.Form):
    bus_no = forms.ModelChoiceField(queryset=Bus.objects.values_list("bus_no", flat=True), required=True)
    seats_available = forms.ChoiceField(choices=[(i, i) for i in range(1, 61)])
    start_place = forms.ModelChoiceField(queryset=Places.objects.values_list("places", flat=True), required=True)
    start_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)
    end_place = forms.ModelChoiceField(queryset=Places.objects.values_list("places", flat=True), required=True)
    end_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)


class UserBookingForm(forms.Form):
    bus_no = forms.ModelChoiceField(queryset=Bus.objects.values_list("bus_no", flat=True), label="Bus number")
    no_of_seats = forms.IntegerField(min_value=1)
    user_pickup_point = forms.CharField()
    user_dropdown_point = forms.CharField()


class CheckAvailabilityForm(forms.Form):
    route_from = forms.ModelChoiceField(queryset=Places.objects.values_list("places", flat=True))
    destination_to = forms.ModelChoiceField(queryset=Places.objects.values_list("places", flat=True))
    date_of_travel = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class EditPlaceForm(forms.Form):
    place_a = forms.ModelChoiceField(queryset=Places.objects.values_list("places", flat=True), label="Select Place")
    place_b = forms.CharField(label="Select Place")
    
class DeletePlaceForm(forms.Form):
    place = forms.ModelChoiceField(queryset=Places.objects.values_list("places", flat=True), label="Select Place")

class EditBusForm(forms.Form):
    BUS_TYPE_CHOICES = [
        ('sleeper', 'Sleeper'),
        ('ac_sleeper', 'AC Sleeper'),
        ('seated', 'Seated'),
        ('ac_seated', 'AC Seated'),
    ]
    bus_id = forms.ModelChoiceField(queryset=Bus.objects.values_list("id", flat=True))
    bus_no = forms.CharField(max_length=20)
    bus_name = forms.CharField(max_length=50)
    total_seats = forms.IntegerField(min_value=20, max_value=60)
    bus_type = forms.ChoiceField(choices=BUS_TYPE_CHOICES)

class DeleteBusForm(forms.Form):
    bus_id = forms.ModelChoiceField(queryset=Bus.objects.values_list("id", flat=True))

class UserFilterForm(forms.Form):
    CHOICES = [
        ('username', 'Username'),
        ('email', 'Email')
    ]
    filter_by = forms.ChoiceField(choices=CHOICES)
    data = forms.CharField()