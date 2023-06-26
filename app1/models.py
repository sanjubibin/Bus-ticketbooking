from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Places(models.Model):
    places = models.CharField(max_length=100, unique=True)

class Bus(models.Model):
    bus_no = models.CharField(max_length=20, unique=True)
    bus_name = models.CharField(max_length=50, unique=True)
    total_seats = models.IntegerField()
    bus_type = models.CharField(max_length=20)

class BusStatus(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    seats_available = models.IntegerField()
    start_place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="bus_starting_place")
    start_date = models.DateField()
    start_time = models.TimeField()
    end_place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name="bus_ending_place")
    end_date = models.DateField()
    end_time = models.TimeField()

class UserBooking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booked_date = models.DateField()
    booked_time = models.TimeField()
    no_of_seats = models.IntegerField()
    busstatus = models.ForeignKey(BusStatus, on_delete=models.CASCADE)
    user_pickup_point = models.CharField()
    user_dropdown_point = models.CharField()
    user_pickup_date = models.DateField()
    user_pickup_time = models.TimeField()
    user_dropdown_date = models.DateField()
    user_dropdown_time = models.TimeField()

