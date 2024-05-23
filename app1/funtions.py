from .models import Places, Bus, BusStatus, UserBooking
from django.contrib.auth.models import User
import ssl
import smtplib
from email.message import EmailMessage
from .credential import mail_password
from django.contrib.auth import logout

def all_places():
    all_places = Places.objects.all().order_by("id")
    data1 = [{"id": place.pk, "place": place.places} for place in all_places]
    return data1


def all_buses():
    buses = Bus.objects.all().order_by("id")
    data2 = [{"id":bus.pk,
            "bus_no": bus.bus_no,
            "bus_name": bus.bus_name,
            "total_seats": bus.total_seats,
            "bus_type": bus.bus_type} for bus in buses]
    return data2


def all_bus_status():
    bus_statuses = BusStatus.objects.all()
    all_bus_status = [{
        "id": bus_status.pk,
        "bus_id": bus_status.bus.pk,
        "seats_available": bus_status.seats_available,
        "start_place_id": bus_status.start_place.pk,
        "start_date": bus_status.start_date,
        "start_time": bus_status.start_time,
        "end_place_id": bus_status.end_place.pk,
        "end_date": bus_status.end_date,
        "end_time": bus_status.end_time
    } for bus_status in bus_statuses]
    return all_bus_status


from datetime import date
def all_bus_status_filter_by_upcoming_date():
    bus_statuses = BusStatus.objects.filter(start_date__gte=date.today()).order_by("-seats_available")
    all_bus_status = [{
        "id": bus_status.pk,
        "bus_id": bus_status.bus.pk,
        "seats_available": bus_status.seats_available,
        "start_place": bus_status.start_place.places,
        "start_date": bus_status.start_date,
        "start_time": bus_status.start_time,
        "end_place": bus_status.end_place.places,
        "end_date": bus_status.end_date,
        "end_time": bus_status.end_time
    } for bus_status in bus_statuses]
    return all_bus_status


def all_bus_status_filter_by_expired_date():
    bus_statuses = BusStatus.objects.filter(start_date__lte=date.today()).order_by("id")
    all_bus_status = [{
        "id": bus_status.pk,
        "bus_id": bus_status.bus.pk,
        "seats_available": bus_status.seats_available,
        "start_place": bus_status.start_place.places,
        "start_date": bus_status.start_date,
        "start_time": bus_status.start_time,
        "end_place": bus_status.end_place.places,
        "end_date": bus_status.end_date,
        "end_time": bus_status.end_time
    } for bus_status in bus_statuses]
    return all_bus_status

     
import datetime
def is_date(data):
    if isinstance(data, datetime.date):
        return True
    else:
        return False
    

def userbookingfilter(user):
        Userbooking = UserBooking.objects.filter(user=user)
        data = [{
            "Name": userbooking.user.username,
            "Email": userbooking.user.email,
            "No_of_seats": userbooking.no_of_seats,
            "Bus_Type": userbooking.busstatus.bus.bus_type,
            "Bus_Name": userbooking.busstatus.bus.bus_name,
            "Bus_No": userbooking.busstatus.bus.bus_no,
            "Pickup_Point": userbooking.user_pickup_point,
            "Pickup_Date": userbooking.user_pickup_date,
            "Pickup_Time": userbooking.user_pickup_time,
            "Dropdown_Point": userbooking.user_dropdown_point,
            "Dropdown_Date": userbooking.user_dropdown_date,
            "Dropdown_Time": userbooking.user_dropdown_time,
            "Bus_Start_point": userbooking.busstatus.start_place.places,
            "Bus_End_Point": userbooking.busstatus.end_place.places,
        } for userbooking in Userbooking]
        return data

def userfilter(user):
     filteruser = User.objects.filter(username=user)
     data = [{
        "id": user.pk,
        "user_name": user.username,
        "email": user.email,
        "is_active": user.is_active,
        "signup_date": user.date_joined,
        "last_login": user.last_login 
     } for user in filteruser]
     return data

def send_mail(message, email):
        msg = message
        user_email =  email

        mail = EmailMessage()
        mail["From"] = "sanjubibin1218124@gmail.com"
        mail["To"] = user_email
        mail["Subject"] = "AS-Travels"
        mail.set_content(msg)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login("sanjubibin1218124@gmail.com", mail_password)
            result = smtp.send_message(mail)
            if not result:
                pass

def logoutsite(request):
    logout(request)
    request.session.flush()


        