from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignInForm
from .forms import BusForm, PlaceForm, UserBookingForm, BusStatusForm, CheckAvailabilityForm, EditPlaceForm, DeletePlaceForm, EditBusForm, DeleteBusForm, UserFilterForm, ProfileForm
from .models import Places, Bus, UserBooking, BusStatus
from django.contrib.auth.decorators import login_required
import re
from django.urls import reverse
from django.db.models import Q
import datetime as dt
import ssl
import smtplib
from email.message import EmailMessage
from .credential import mail_password, mail_username
from .funtions import (all_places, all_buses, all_bus_status, userbookingfilter, 
                       send_mail, all_bus_status_filter_by_upcoming_date, 
                       all_bus_status_filter_by_expired_date, userfilter, logoutsite)

#Rest framework

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import (PlacesSerializer, BusSerializer, BusStatusSerializer, 
                        UserBookingSerializer, SignUpApiSerializer, LogInApiSerializer,
                        MediaUploadSerializer, UserSerializer)
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken
from rest_framework_simplejwt.authentication import JWTAuthentication
#code here

def swagger_ui(request):
    return render(request, 'swagger_custom.html')

class SignUp(View):
    def get(self, request):
        form = SignInForm()
        return render(request, "app1/signup.html", {"form": form})
    
    def post(self, request):
        form = SignInForm(self.request.POST)
        if form.is_valid():
            username = self.request.POST.get('username')
            email = self.request.POST.get('email')
            password1 = self.request.POST.get('password1')
            password2 = self.request.POST.get('password2')

            if User.objects.filter(email=email).exists():
                message = "User with this email is already registered."
                return render(request, "app1/signup.html", {"form": form, "message": message})

            if password1 != password2:
                message = "Passwords do not match."
                return render(request, "app1/signup.html", {"form": form, "message": message})
            
            if (
                len(password1) < 8
                or not re.search(r'[A-Z]', password1)
                or not re.search(r'[a-z]', password1)
                or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1)
            ):
                message = "Password must be at least 8 characters long \nand contain at least one uppercase letter, \none lowercase letter, and one special character."
                return render(request, "app1/signup.html", {"form": form, "message": message})

            if password1 == password2 and not User.objects.filter(email=email).exists():
                User.objects.create_user(username=username, email=email, password=password1)
                send_mail("You Are successfully signedup to \"AS Travels\" \n We will keep you updated for news", email)
                return render(request, "app1/login.html")

        return render(request, "app1/signup.html", {"form": form})
    

class SignUpApi(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        form = SignInForm(self.request.POST)
        if form.is_valid():
            username = self.request.POST.get('username')
            email = self.request.POST.get('email')
            password1 = self.request.POST.get('password1')
            password2 = self.request.POST.get('password2')

            if User.objects.filter(email=email).exists():
                message = "User with this email already registered."
                data = SignUpApiSerializer({"message": message})
                return Response(data.data)

            if User.objects.filter(username=username).exists():
                message = "User with this username already registered."
                data = SignUpApiSerializer({"message": message})
                return Response(data.data)

            if password1 != password2:
                message = "Passwords do not match."
                data = SignUpApiSerializer({"message": message})
                return Response(data.data)
            
            if (
                len(password1) < 8
                or not re.search(r'[A-Z]', password1)
                or not re.search(r'[a-z]', password1)
                or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1)
            ):
                message = "Password must be at least 8 characters long \n and contain at least one uppercase letter, \none lowercase letter, and one special character."
                data = SignUpApiSerializer({"message": message})
                return Response(data.data)

            if password1 == password2 and not User.objects.filter(email=email).exists():
                User.objects.create_user(username=username, email=email, password=password1)
                send_mail("You Are successfully signedup to \" AS Travels \" We will keep you updated for news", email)
                message = "you are successfully logged in check mail for confirmation"
                data = SignUpApiSerializer({"message": message, "logged_username": username, "logged_email": email})
                return Response(data.data)


class LogIn(View):
    def get(self, request):
        return render(request, "app1/login.html")
    
    def post(self, request):
        email = self.request.POST.get("email")
        password = self.request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "app1/login.html", {"msg": f"No user with this email '{email}' has registered yet"})
        
        auth_user = authenticate(request, username=user.username, email= user.email, password=password)
        if auth_user is not None and not user.is_superuser:
            login(request, auth_user)
            return redirect("homepage")
        elif auth_user is not None and user.is_superuser:
            login(request, auth_user)
            return redirect("adminpage")
        else:
            msg = "Invalid username or password"
            return render(request, "app1/login.html", {"msg": msg})
        
from rest_framework.authtoken.models import Token
        
class LoginView(APIView):
    def post(self, request):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            msg = f"No user with this username '{username}' has registered yet"
            data = LogInApiSerializer({"message": msg})
            return Response(data.data)
        
        auth_user = authenticate(username=username, password=password)

        if auth_user is not None and not user.is_superuser:
            login(self.request, auth_user)
            token = Token.objects.get_or_create(user=auth_user)[0]
            msg = "you are logged in as User"
            return Response({"message": msg, "logged_user_email": user.email, "token": f"Token {token.key}"})

        elif auth_user is not None and user.is_superuser:
            login(self.request, auth_user)
            token = Token.objects.get_or_create(user=auth_user)[0]
            msg = "you are logged in as Admin user"
            return Response({"message": msg, "logged_user_email": user.email, "token":  f"Token {token.key}"})
        
        else:
            msg = "Invalid username or password"
            data = LogInApiSerializer({"message": msg})
            return Response(data.data)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = self.request.user
        logout(self.request)
        self.request.session.flush()
        Token.objects.filter(user=user).delete()
        return Response({"message": "successfully logged out"})


class Home(LoginRequiredMixin, View):
    def get(self, request): 
        form = UserBookingForm()
        username = self.request.user.username
        return render(request, "app1/home.html", {"form": form, "username": username, "places": all_places, "buses":all_buses, "all_bus_status": all_bus_status_filter_by_upcoming_date})
    
    def post(self, request):
        form = UserBookingForm()
        username = self.request.user.username
        return render(request, "app1/home.html", {"form": form, "username": username})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

from rest_framework.authentication import TokenAuthentication
from datetime import date  
class HomeApi(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        username = self.request.user.username
        places = Places.objects.all()
        places_serial = PlacesSerializer(places, many=True)
        bus = Bus.objects.all()
        bus_serial = BusSerializer(bus, many=True)
        all_bus_active = BusStatus.objects.filter(start_date__gte=date.today()).order_by("id")
        all_bus_active_serial = BusStatusSerializer(all_bus_active, many=True)
        return Response({"username": username, "places": places_serial.data, "buses": bus_serial.data, "all_upcoming_bus_status": all_bus_active_serial.data})

    
class BookTicket(LoginRequiredMixin, View):
    def get(self, request):
        form = UserBookingForm()
        is_it = False
        bus_nos = None
        if self.request.session.get("checkavailability_bus_no"):
            is_it = True
            bus_nos = self.request.session.get("checkavailability_bus_no")
        return render(request, "app1/bookticket.html", {"form": form, "is_it": is_it, "bus_select": f"Select The Bus No \"{bus_nos}\" That Suits Your Request"})

    def post(self, request):
        form = UserBookingForm(self.request.POST)

        auth_user = self.request.user

        bus_no = self.request.POST.get("bus_no")
        no_of_seats = self.request.POST.get("no_of_seats")
        pickup_place = self.request.POST.get("user_pickup_point")
        dropdown_place = self.request.POST.get("user_dropdown_point")
        wholebus = Bus.objects.get(bus_no=bus_no)
        wholebus_busstatus = BusStatus.objects.get(bus_id=wholebus.id)

        total_seats = wholebus_busstatus.seats_available

        if int(total_seats)+1 <= int(no_of_seats):
            return render(request, "app1/bookticket.html", {"form": form,
                                                            "error": f"Only {wholebus_busstatus.seats_available} seats remaining"})

        data = UserBooking(
            user=auth_user,
            booked_date=dt.datetime.now().date(),
            booked_time=dt.datetime.now().time(),
            no_of_seats=no_of_seats,
            busstatus=wholebus_busstatus,
            user_pickup_point=pickup_place,
            user_dropdown_point=dropdown_place,
            user_pickup_date=wholebus_busstatus.start_date,
            user_pickup_time=wholebus_busstatus.start_time,
            user_dropdown_date=wholebus_busstatus.end_date,
            user_dropdown_time=wholebus_busstatus.end_time
        )
        try:
            data.save()
            wholebus_busstatus.seats_available = int(wholebus_busstatus.seats_available) - int(no_of_seats)
            wholebus_busstatus.save()
            if "checkavailability_bus_no" in self.request.session:
                del self.request.session["checkavailability_bus_no"]
            self.request.session["body_content"] = f"""your booking from pickup point:\"{pickup_place}\" to dropdown point:\"{dropdown_place}\" has been confirmed. For your info that bus will start from \"{wholebus_busstatus.start_place.places}\" to \"{wholebus_busstatus.end_place.places}\""""
            self.request.session["email"] = data.user.email
            return redirect(reverse("confirmmail"))
        except:
            return render(request, "app1/bookticket.html", {"form": form, "msg": "Something went wrong"})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

class BookTicketApi(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        auth_user = self.request.user

        bus_no = self.request.POST.get("bus_no")
        no_of_seats = self.request.POST.get("no_of_seats")
        pickup_place = self.request.POST.get("user_pickup_point")
        dropdown_place = self.request.POST.get("user_dropdown_point")
        wholebus = Bus.objects.get(bus_no=bus_no)
        wholebus_busstatus = BusStatus.objects.get(bus_id=wholebus.id)

        total_seats = wholebus_busstatus.seats_available

        if int(total_seats)+1 <= int(no_of_seats):
            return Response({"error": f"Only {wholebus_busstatus.seats_available} seats remaining"})

        data = UserBooking(
            user=auth_user,
            booked_date=dt.datetime.now().date(),
            booked_time=dt.datetime.now().time(),
            no_of_seats=no_of_seats,
            busstatus=wholebus_busstatus,
            user_pickup_point=pickup_place,
            user_dropdown_point=dropdown_place,
            user_pickup_date=wholebus_busstatus.start_date,
            user_pickup_time=wholebus_busstatus.start_time,
            user_dropdown_date=wholebus_busstatus.end_date,
            user_dropdown_time=wholebus_busstatus.end_time
        )
        try:
            data.save()
            wholebus_busstatus.seats_available = int(wholebus_busstatus.seats_available) - int(no_of_seats)
            wholebus_busstatus.save()
            if "checkavailability_bus_no" in self.request.session:
                del self.request.session["checkavailability_bus_no"]
            self.request.session["body_content"] = f"""your booking from pickup point:\"{pickup_place}\" to dropdown point:\"{dropdown_place}\" has been confirmed. For your info that bus will start from \"{wholebus_busstatus.start_place.places}\" to \"{wholebus_busstatus.end_place.places}\""""
            self.request.session["email"] = data.user.email
            return Response({"msg": "successfully booked ticket. check mail for confirmation"})
        except:
            return Response({"msg": "Something went wrong"})

class SendMail(View):
    def get(self, request):
        try:
            msg = self.request.session.get("body_content")
            user_email = self.request.session.get("email")  
            del self.request.session["body_content"]
            del self.request.session["email"]     

            mail = EmailMessage()
            mail["From"] = mail_username
            mail["To"] = user_email
            mail["Subject"] = "AS-Travels"
            mail.set_content(msg)

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(mail_username, mail_password)
                smtp.send_message(mail)
                return render(request, "app1/mail.html")
        except KeyError:
            message = "Invalid Access to This Page"            
            return render(request, "error.html", {"message": message})
        
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    

class CheckAvailability(LoginRequiredMixin, View):

    def get(self, request):
        form = CheckAvailabilityForm()
        return render(request, "app1/check_bus.html", {"form": form})
    
    def post(self, request):
        form = CheckAvailabilityForm()
        pickup_point = self.request.POST.get("route_from")
        pickup_point_id = Places.objects.get(places =pickup_point) 

        date = self.request.POST.get("date_of_travel")

        drop_point = self.request.POST.get("destination_to")
        drop_point_id = Places.objects.get(places = drop_point)

        available_bus = BusStatus.objects.filter(
                Q(start_place__exact=pickup_point_id) & 
                Q(start_date__exact=date) & 
                Q(end_place__exact=drop_point_id)
            ).order_by("seats_available")
        if available_bus:
            Bus = available_bus.order_by("-seats_available")
            data1 = [{
                "Bus_no": bus.bus.bus_no,
                "Available_Seats":bus.seats_available,
                "Starting_place":bus.start_place.places,
                "Starting_date":bus.start_date.strftime('%Y-%m-%d'),
                "Starting_time":bus.start_time.strftime('%H:%M:%S'),
                "Destination_place":bus.end_place.places,
                "Destination_date":bus.end_date.strftime('%Y-%m-%d'),
                "Destination_time":bus.end_time.strftime('%H:%M:%S')
            } for bus in Bus]
            session_bus = available_bus.last()
            session_bus_no = session_bus.bus.bus_no
            self.request.session["checkavailability_bus_no"] = session_bus_no
            return render(request, "app1/checkavailabilityresults.html", {"data1": data1})
        else:
            no_bus = "No available bus for your requirements"
        return render(request, "app1/check_bus.html", {"form": form, "no_bus": no_bus}) 
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    
    
class CheckAvailabilityApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            pickup_point = self.request.POST.get("route_from")
            pickup_point_id = Places.objects.get(places =pickup_point) 

            aa = self.request.POST.get("date_of_travel")
            date = aa

            drop_point = self.request.POST.get("destination_to")
            drop_point_id = Places.objects.get(places = drop_point)

            available_bus = BusStatus.objects.filter(
                    Q(start_place__exact=pickup_point_id) & 
                    Q(start_date__exact=date) & 
                    Q(end_place__exact=drop_point_id)
                )
            if available_bus:
                Bus = available_bus
                data1 = [{
                    "Bus_no": bus.bus.bus_no,
                    "Available_Seats":bus.seats_available,
                    "Starting_place":bus.start_place.places,
                    "Starting_date":bus.start_date.strftime('%Y-%m-%d'),
                    "Starting_time":bus.start_time.strftime('%H:%M:%S'),
                    "Destination_place":bus.end_place.places,
                    "Destination_date":bus.end_date.strftime('%Y-%m-%d'),
                    "Destination_time":bus.end_time.strftime('%H:%M:%S')
                } for bus in Bus]
                session_bus = available_bus.first()
                session_bus_no = session_bus.bus.bus_no
                self.request.session["checkavailability_bus_no"] = session_bus_no
                return Response({"filtered bus": data1})
        except:
            no_bus = "No available bus for your requirements"
            return Response({"msg": no_bus}) 
        

class UserBookingDetails(LoginRequiredMixin, View):
    def get(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id = user_id)
        Userbooking = UserBooking.objects.filter(user=user)
        display_data = [{
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
        return render(request, "app1/userdetail.html", {"Display": display_data})
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

class UserBookingDetailsApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = self.request.user.id
        user = User.objects.get(id = user_id)
        Userbooking = UserBooking.objects.filter(user=user)
        display_data = [{
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
        return Response({"User_bboking_details": display_data})



##########  --ADMIN PAGE--   ##########



class PlaceAdd(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_superuser:
            return redirect(reverse("logout"))
        form = PlaceForm
        return render(request, "app1/admin/place_add.html", {"form": form, "places": all_places()})

    def post(self, request):
        form = PlaceForm(self.request.POST)
        places = self.request.POST.get("places")
        if form.is_valid() and not Places.objects.filter(places=places).exists():
            form.save()
            return render(request, "app1/admin/place_add.html", {"form": PlaceForm, "msg": f"Place \"{places}\" added successfully", "places": all_places()})
        else:
            return render(request, "app1/admin/place_add.html", {"form": PlaceForm, "msg": "Place already exists", "places": all_places()})
        
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    
class PlaceAddApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.user.is_superuser:
            logoutsite(self.request)
            self.request.session.flush()
            return Response({"msg": "you have been logged out because this page is only accessible by admin"})
        places = Places.objects.all()
        data = PlacesSerializer(places, many=True)
        return Response({"places that already exists": data.data})
    
    def post(self, request):
        if not self.request.user.is_superuser:
            logoutsite(self.request)
            self.request.session.flush()
            return Response({"msg": "you have been logged out due to because this page is only accessible by admin"})
        form = PlaceForm(self.request.POST)
        places = self.request.POST.get("places")
        data = PlacesSerializer(Places.objects.all(), many=True)
        if form.is_valid() and not Places.objects.filter(places=places).exists():
            form.save()
            return Response({"msg": f"Place '{places}' added successfully", "places that already exist": data.data})
        else:
            return Response({"msg": "Place that you entered already exists", "places that already exist": data.data})
        
    
class PlaceEdit(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_superuser:
            return redirect(reverse("logout"))
        form = EditPlaceForm
        return render(request, "app1/admin/place_edit.html", {"form": form, "places": all_places()})
    
    def post(self, request):
        form = EditPlaceForm(self.request.POST)

        place_id = self.request.POST.get("place_a")
        place = self.request.POST.get("place_b")
        if not Places.objects.filter(places=place).exists():
            place_model = Places.objects.get(places=place_id)
            place_model.places = place
            place_model.save()
            return render(request, "app1/admin/place_edit.html", {"form": EditPlaceForm, "places": all_places, "msg": f"place '{place}' with place id '{place_id} has successfully edited"})
        else:
            return render(request, "app1/admin/place_edit.html", {"form": EditPlaceForm, "places": all_places, "msg": "This place already exists"})
        

class PlaceEditApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.user.is_superuser:
            logoutsite(self.request)
            self.request.session.flush()
            return Response({"msg": "you have been logged out because this page is only accessible by admin"})
        places = Places.objects.all()
        data = PlacesSerializer(places, many=True)
        return Response({"places": data.data})
    
    def post(self, request):
        if not self.request.user.is_superuser:
            logout(self.request)
            self.request.session.flush()
            return Response({"msg": "you have been logged out because this page is only accessible by admin"})
        place_id = self.request.POST.get("place_id")
        place = self.request.POST.get("place")
        data = PlacesSerializer(Places.objects.all(), many=True)
        if not Places.objects.filter(places=place).exists():
            place_model = Places.objects.get(pk=place_id)
            place_model.places = place
            place_model.save()
            return Response({"msg": f"place '{place}' with place id '{place_id} has successfully edited", "places": data.data})
        else:
            return Response({"msg": "This place already exists", "places": data.data})
        

class PlaceDelete(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_superuser:
            return redirect(reverse("logout"))
        form = DeletePlaceForm
        return render(request, "app1/admin/place_delete.html", {"form": form, "places": all_places})

    def post(self, request):
        form = DeletePlaceForm(self.request.POST)
        
        place_id = self.request.POST.get("place")
        if Places.objects.filter(places=place_id).exists():
            place_model = Places.objects.get(places=place_id)
            place_model.delete()
            return render(request, "app1/admin/place_delete.html", {"form": DeletePlaceForm, "places": all_places, "msg": f"place place id \"{place_id}\" has successfully deleted"})
        else:
            data1 = [{"place_id": place.pk, "place": place.places} for place in all_places]
            return render(request, "app1/admin/place_edit.html", {"form": DeletePlaceForm, "places": data1, "msg": "Something Went Wrong"})
        
class PlaceDeleteApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.user.is_superuser:
            logoutsite(self.request)
            self.request.session.flush()
            return Response({"msg": "you have been logged out because this page is only accessible by admin"})
        places = Places.objects.all()
        data = PlacesSerializer(places, many=True)
        return Response({"places": data.data})
    
    def post(self, request):
        
        place_id = self.request.POST.get("place_id")
        data = PlacesSerializer(Places.objects.all(), many=True)
        if Places.objects.filter(pk=place_id).exists():
            place_model = Places.objects.get(pk=place_id)
            place_model.delete()
            return Response({"places": data.data, "msg": f"place place id '{place_id}' has successfully deleted"})
        else:
            return Response({"places": data.data, "msg": "Something Went Wrong"})


class BusAdd(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_superuser:
            return redirect(reverse("logout"))
        form = BusForm
        return render(request, "app1/admin/bus_add.html", {"form": form, "buses": all_buses})

    def post(self, request):
        form = BusForm(self.request.POST)
        bus_no = self.request.POST.get("bus_no")
        if form.is_valid() and not Bus.objects.filter(bus_no=bus_no).exists():
            form.save()
            return render(request, "app1/admin/bus_add.html", {"form": BusForm, "buses": all_buses, "msg": "Bus added successfully"})
        else:
            return render(request, "app1/admin/bus_add.html", {"form": BusForm, "buses": all_buses, "msg": "Bus already exist"})
        
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    

class BusAddApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.user.is_superuser:
            logoutsite(self.request)
            self.request.session.flush()
            return Response({"msg": "you have been logged out because this page is only accessible by admin"})
        data = BusSerializer(Bus.objects.all(), many=True)
        return Response({"buses": data.data})
    
    def post(self, request):
        bus_no = self.request.POST.get("bus_no")
        bus_name = self.request.POST.get("bus_name")
        total_seats = self.request.POST.get("total_seats")
        bus_type = self.request.POST.get("bus_type")
        all_bus = BusSerializer(Bus.objects.all(), many=True)
        if not Bus.objects.filter(bus_no=bus_no).exists():
            data = Bus(bus_no=bus_no, bus_name=bus_name, total_seats=total_seats, bus_type=bus_type)
            data.save()
            return Response({"msg": "Bus added successfully", "buses": all_bus.data})
        else:
            return Response({"msg": "Bus already exist", "buses": all_bus.data})

class BusEdit(LoginRequiredMixin, View):

    def get(self, request):
        if not self.request.user.is_superuser:
            return redirect(reverse("logout"))
        form = EditBusForm
        return render(request, "app1/admin/bus_edit.html", {"form": form, "buses": all_buses})
    
    def post(self, request):
        form = EditBusForm(self.request.POST)
        bus_id = self.request.POST.get("bus_id")
        bus_no = self.request.POST.get("bus_no")
        bus_name = self.request.POST.get("bus_name")
        total_seats = self.request.POST.get("total_seats")
        bus_type = self.request.POST.get("bus_type")
        try:
            bus = Bus.objects.get(id=bus_id)
            bus.bus_no = bus_no
            bus.bus_name = bus_name
            bus.total_seats = total_seats
            bus.bus_type = bus_type
            bus.save()
            return render(request, "app1/admin/bus_edit.html", {"form": EditBusForm, "buses": all_buses, "msg": f"bus with the Bus Id of {bus_id} has been Edited"})
        except:
            if Bus.objects.filter(bus_no=bus_no).exists() and Bus.objects.filter(bus_name=bus_name).exists():
                bus = Bus.objects.get(id=bus_id)
                bus.total_seats = total_seats
                bus.bus_type = bus_type
                bus.save()
                return render(request, "app1/admin/bus_edit.html", {"form": EditBusForm, "buses": all_buses, "msg": "Only Total Seats and Bus Type has been updated"})
            else:
                return render(request, "app1/admin/bus_edit.html", {"form": EditBusForm, "buses": all_buses, "msg": "Bus with this Bus  or Bus Name already exist"})
 

class BusEditApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.user.is_superuser:
            logout(self.request)
            self.request.session.flush()
            return Response({"msg": "you have been logged out because this page is only accessible by admin"})
        data = BusSerializer(Bus.objects.all(), many=True)
        return Response({"buses": data.data})
    
    def post(self, request):
        bus_id = self.request.POST.get("bus_id")
        bus_no = self.request.POST.get("bus_no")
        bus_name = self.request.POST.get("bus_name")
        total_seats = self.request.POST.get("total_seats")
        bus_type = self.request.POST.get("bus_type")
        all_bus = BusSerializer(Bus.objects.all(), many=True)
        try:
            bus = Bus.objects.get(id=bus_id)
            bus.bus_no = bus_no
            bus.bus_name = bus_name
            bus.total_seats = total_seats
            bus.bus_type = bus_type
            bus.save()
            return Response({"msg": f"bus with the Bus Id of {bus_id} has been Edited", "buses": all_bus.data})
        except:
            if Bus.objects.filter(bus_no=bus_no).exists() and Bus.objects.filter(bus_name=bus_name).exists():
                bus = Bus.objects.get(id=bus_id)
                bus.total_seats = total_seats
                bus.bus_type = bus_type
                bus.save()
                return Response({"msg": "Only Total Seats and Bus Type has been updated", "buses": all_bus.data})
            else:
                return Response({"msg": "Bus with this Bus  or Bus Name already exist", "buses": all_bus.data})

class BusDelete(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_superuser:
            return redirect(reverse("logout"))
        form = DeleteBusForm
        return render(request, "app1/admin/bus_delete.html", {"form": form, "buses": all_buses})

    def post(self, request):
        form = DeleteBusForm(self.request.POST)
        bus_id = self.request.POST.get("bus_id")

        try:
            bus = Bus.objects.get(id=bus_id)
            bus.delete()
            return render(request, "app1/admin/bus_delete.html", {"form": DeleteBusForm, "buses": all_buses, "msg": f"Bus with the selected Bus Id \"{bus_id}\" has been deleted"})
        except:
            return render(request, "app1/admin/bus_delete.html", {"form": DeleteBusForm, "buses": all_buses, "msg": "Something Went Wrong"})

class BusDeleteApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not self.request.user.is_superuser:
            logout(self.request)
            self.request.session.flush()
            return Response({"msg": "you have been logged out because this page is only accessible by admin"})
        data = BusSerializer(Bus.objects.all(), many=True)
        return Response({"buses": data.data})

    def post(self, request):
        bus_id = self.request.POST.get("bus_id")
        data = BusSerializer(Bus.objects.all(), many=True)
        try:
            bus = Bus.objects.get(id=bus_id)
            bus.delete()
            return Response({"msg": f"Bus with the selected Bus Id \"{bus_id}\" has been deleted", "buses": data.data})
        except:
            return Response({"msg": "Something Went Wrong", "buses": data.data})


class AdminPage(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_superuser:
            return redirect(reverse("logout"))
        all_places = Places.objects.all()
        data1 = [{"place_id": place.pk, "place": place.places} for place in all_places]
        self.request.session["places"] = data1
        return render(request, "app1/admin/admin.html")

    def post(self, request):
        if not self.request.user.is_superuser:
            return render(request, "display.html", {"msg": "UnAuthorised Access to this page", "msg2": "Login properly to access this page"})
        return render(request, "app1/admin/admin.html")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    
class AdminPageApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not self.request.user.is_superuser:
            logout(self.request)
            self.request.session.flush()
            return Response({"msg": "you are logged out due to UnAuthorised Access to this page.Login properly to access this page"})
        return Response({"msg": "you are logged in as admin user"})


class FilterUser(LoginRequiredMixin, View):
    def get(self, request):
        form = UserFilterForm
        return render(request, "app1/admin/filter_user.html", {"form": form})
    
    def post(self, request):
        form = UserFilterForm(self.request.POST)
        choice = self.request.POST.get("filter_by")
        data = self.request.POST.get("data")

        try:
            if choice == "username":
                if User.objects.filter(username=data).exists():
                    user = User.objects.get(username=data)
                data1 = userbookingfilter(user)
                data2 = userfilter(user.username)
                return render(request, "app1/admin/filter_user.html", {"form": UserFilterForm, "data1": data1, "data2": data2})
            
            elif choice == "email":
                if User.objects.filter(email=data).exists():
                    user = User.objects.get(email=data)
                data1 = userbookingfilter(user)
                data2 = userfilter(user.username)
                return render(request, "app1/admin/filter_user.html", {"form": UserFilterForm, "data1": data1, "data2": data2})
        except:
            return render(request, "app1/admin/filter_user.html", {"form": UserFilterForm, "error": "Details you entered mismatched or wrong"})
        
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

class FilterUserApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        try:
            choice = self.request.POST.get("filter_by")
            data = self.request.POST.get("data")
            if choice == "username":
                if User.objects.filter(username=data).exists():
                    user = User.objects.get(username=data)
                data1 = userbookingfilter(user)
                data2 = userfilter(user.username)
                return Response({"user booking details": data1, "user details": data2})
            
            elif choice == "email":
                if User.objects.filter(email=data).exists():
                    user = User.objects.get(email=data)
                data1 = userbookingfilter(user)
                data2 = userfilter(user.username)
                return Response({"user booking details": data1, "user details": data2})
        except:
            return Response({"error": "Details you entered mismatched or wrong"})


class BusStatusAdd(LoginRequiredMixin, View):
    def get(self, request):
        if not self.request.user.is_superuser:
            return redirect(reverse("logout", {"msg_unauth": "you are logged out due to unautherised access to this page"}))
        form = BusStatusForm()
        buses = Bus.objects.all()
        data2 = [{"bus id":bus.pk,
                "bus no": bus.bus_no,
                "bus_name": bus.bus_name,
                "total seats": bus.total_seats,
                "bus_type": bus.bus_type} for bus in buses]
        return render(request, "app1/admin/busstatus_add.html", {"form": form, "buses": data2, 
                                                                "all_bus_status_filter_by_expired_date": all_bus_status_filter_by_expired_date,
                                                                "all_bus_status_filter_by_upcoming_date": all_bus_status_filter_by_upcoming_date,
                                                                 })

    def post(self, request):
        form = BusStatusForm(self.request.POST)
        bus_no = self.request.POST.get("bus_no")
        bus_start_place = self.request.POST.get("start_place")
        bus_end_place = self.request.POST.get("end_place")
        startdate = self.request.POST.get("start_date")
        starttime = self.request.POST.get("start_time")
        enddate = self.request.POST.get("end_date")
        endtime = self.request.POST.get("end_time")

        bus = Bus.objects.get(bus_no=bus_no)

        if not BusStatus.objects.filter(bus=bus).exists():
            start_place = Places.objects.get(places=bus_start_place)
            end_place = Places.objects.get(places=bus_end_place)

            data = BusStatus(
                bus=Bus.objects.get(bus_no=bus_no),
                seats_available=self.request.POST.get("seats_available"),
                start_place=start_place,
                start_date=startdate,
                start_time=starttime,
                end_place=end_place,
                end_date=enddate,
                end_time=endtime
            )
            data.save()
            buses = Bus.objects.all()
            data2 = [{"bus id":bus.pk,
                "bus no": bus.bus_no,
                  "bus_name": bus.bus_name,
                  "total seats": bus.total_seats,
                  "bus_type": bus.bus_type} for bus in buses]
            return render(request, "app1/admin/busstatus_add.html", {"form": BusStatusForm,"buses": data2, "all_bus_status_filter_by_expired_date": all_bus_status_filter_by_expired_date,
                                                                     "all_bus_status_filter_by_upcoming_date": all_bus_status_filter_by_upcoming_date,
                                                                      "msg": f"Bus from {bus_start_place} to {bus_end_place} starting on {startdate} added successfully"})
        
        else:
            buses = Bus.objects.all()
            data2 = [{"bus id":bus.pk,
                "bus no": bus.bus_no,
                "bus_name": bus.bus_name,
                "total seats": bus.total_seats,
                "bus_type": bus.bus_type} for bus in buses]
            return render(request, "app1/admin/busstatus_add.html", {"form": BusStatusForm, "all_bus_status_filter_by_expired_date": all_bus_status_filter_by_expired_date,
                                                                     "all_bus_status_filter_by_upcoming_date": all_bus_status_filter_by_upcoming_date,"buses": data2, "msg": "Bus with the given number already exists"})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    
class BusStatusAddApi(APIView):
    permission_classes = [IsAuthenticated]

    global all_bus, expired_bus_statuses_serializer, upcoming_bus_statuses_serializer

    all_bus = BusSerializer(Bus.objects.all(), many=True)
    expired_bus_statuses = BusStatus.objects.filter(start_date__lte=date.today()).order_by("id")
    expired_bus_statuses_serializer = BusStatusSerializer(expired_bus_statuses, many=True)
    upcoming_bus_statuses = BusStatus.objects.filter(start_date__gte=date.today()).order_by("id")
    upcoming_bus_statuses_serializer = BusStatusSerializer(upcoming_bus_statuses, many=True)

    def get(self, request):
        if not self.request.user.is_superuser:
            logout(self.request)
            self.request.session.flush()

        return Response({"buses": all_bus.data, 
                        "all_bus_status_filter_by_expired_date": expired_bus_statuses_serializer.data,
                        "all_bus_status_filter_by_upcoming_date": upcoming_bus_statuses_serializer.data
                            })

    def post(self, request):
        form = BusStatusForm(self.request.POST)
        bus_no = self.request.POST.get("bus_no")
        bus_start_place = self.request.POST.get("start_place")
        bus_end_place = self.request.POST.get("end_place")
        startdate = self.request.POST.get("start_date")
        starttime = self.request.POST.get("start_time")
        enddate = self.request.POST.get("end_date")
        endtime = self.request.POST.get("end_time")
        seatsavailalble = self.request.POST.get("seats_available")
        bus = Bus.objects.get(bus_no=bus_no)

        if not BusStatus.objects.filter(bus=bus).exists():
            start_place = Places.objects.get(places=bus_start_place)
            end_place = Places.objects.get(places=bus_end_place)

            data = BusStatus(
                bus=Bus.objects.get(bus_no=bus_no),
                seats_available=seatsavailalble,
                start_place=start_place,
                start_date=startdate,
                start_time=starttime,
                end_place=end_place,
                end_date=enddate,
                end_time=endtime
            )
            data.save()
            buses = Bus.objects.all()
            data2 = [{"bus id":bus.pk,
                "bus no": bus.bus_no,
                  "bus_name": bus.bus_name,
                  "total seats": bus.total_seats,
                  "bus_type": bus.bus_type} for bus in buses]
            return Response({"msg": f"Bus from {bus_start_place} to {bus_end_place} starting on {startdate} added successfully", "buses": data2, "all_bus_status_filter_by_expired_date": expired_bus_statuses_serializer.data,
                            "all_bus_status_filter_by_upcoming_date": upcoming_bus_statuses_serializer.data})
        
        else:
            buses = Bus.objects.all()
            data2 = [{"bus id":bus.pk,
                "bus no": bus.bus_no,
                "bus_name": bus.bus_name,
                "total seats": bus.total_seats,
                "bus_type": bus.bus_type} for bus in buses]
            return Response({"msg": "Bus with the given number already exists", "all_bus_status_filter_by_expired_date": expired_bus_statuses_serializer.data,
                            "all_bus_status_filter_by_upcoming_date": upcoming_bus_statuses_serializer.data,"buses": data2})

class LogOutSite(APIView):
    def get(self, request):
        logout(request)
        self.request.session.flush()
        return render(request, "app1/logout.html")

# class LogOutApi(APIView):
#     def get(self, request):
#         logout(self.request)
#         self.request.session.flush()
#         return Response({"msg": "you have been logged out"})
    
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authentication import SessionAuthentication

# class LogOutApi(APIView):
#     authentication_classes = (SessionAuthentication,)

#     def get(self, request, *args, **kwargs):
#         self.request.user.access_token.delete()
#         return Response({"msg": "You have been logged out successfully"})

# class LogOutApi(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         token = self.request.POST.get('refresh_token')
#         if token:
#             try:
#                 refresh_token = RefreshToken(token)
#                 refresh_token.blacklist()
#                 return Response({'status': 'ok'})
#             except Exception as e:
#                 return Response({'status': 'error', 'message': str(e)})
#         else:
#             return Response({'status': 'error', 'message': 'Token not provided'})
        #     except Exception as e:
        #         return Response({"message": "Invalid token"})
        # else:
        #     return Response({"message": "Refresh token is required"})

        # return Response({"message": "User logged out successfully"})

#from rest_framework_simplejwt.tokens import AccessToken
import base64

class LogOutApi(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        logout(self.request)
        # authentication = JWTAuthentication()
        # # try:
        # auth_header = authentication.get_header(request)
        # raw_token = authentication.get_raw_token(auth_header)
        # decoded_token = base64.b64encode(str(raw_token).encode('utf-8'))
        # access_token = RefreshToken(decoded_token)

        # access_token.blacklist()

        return Response({'status': 'ok'})
        # except Exception as e:
        #     return Response({'status': 'error', 'message': str(e)})



################  functions shortcuts  ###############

from .forms import ProfileForm
from .models import MediaUpload

class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm()
        return render(request, "app1/user_additional.html", {"form": form})
    
    def post(self, request):
        form = ProfileForm(self.request.POST, self.request.FILES)
        logged_username = self.request.user.username
        user = User.objects.get(username=logged_username)
        file = self.request.FILES.get("user_image")
        address = self.request.POST.get("address")
        mobile = self.request.POST.get("mobile")
        first_name = self.request.POST.get("first_name")
        last_name = self.request.POST.get("last_name")
        if not MediaUpload.objects.filter(user_id=user.pk).exists():
            media = MediaUpload(user=user,
                                file=file,
                                address=address,
                                mobile=mobile)
            media.save()
            adduser = User.objects.get(username=logged_username)
            adduser.first_name = first_name
            adduser.last_name = last_name
            adduser.save()
            return render(request, "app1/user_additional.html", {"form": ProfileForm, "msg": "user profile updated successfully"})


        if MediaUpload.objects.filter(user_id=user.pk).exists():
            media = MediaUpload.objects.get(user=user)
            media.file = file
            media.address = address
            media.mobile = mobile
            media.save()
            adduser = User.objects.get(username=logged_username)
            adduser.first_name = first_name
            adduser.last_name = last_name
            adduser.save()
            return render(request, "app1/user_additional.html", {"form": ProfileForm, "msg": "user profile updated successfully"})
        return render(request, "app1/user_additional.html", {"form": ProfileForm}) 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)

class EditProfileViewApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"msg": "you are logged in as user"})
    
    def post(self, request):
        form = ProfileForm(self.request.POST, self.request.FILES)
        logged_username = self.request.user.username
        user = User.objects.get(username=logged_username)
        file = self.request.FILES.get("user_image")
        address = self.request.POST.get("address")
        mobile = self.request.POST.get("mobile")
        first_name = self.request.POST.get("first_name")
        last_name = self.request.POST.get("last_name")

        if not MediaUpload.objects.filter(user_id=user.pk).exists():
            media = MediaUpload(user=user,
                                file=file,
                                address=address,
                                mobile=mobile)
            media.save()
            adduser = User.objects.get(username=logged_username)
            adduser.first_name = first_name
            adduser.last_name = last_name
            adduser.save()
            return Response({"msg": "user profile updated successfully"})


        if MediaUpload.objects.filter(user_id=user.pk).exists():
            media = MediaUpload.objects.get(user=user)
            media.file = file
            media.address = address
            media.mobile = mobile
            media.save()
            adduser = User.objects.get(username=logged_username)
            adduser.first_name = first_name
            adduser.last_name = last_name
            adduser.save()
            return Response({"msg": "user profile updated successfully"})


class ViewProfile(LoginRequiredMixin, View):
    
    def get(self, request):
        logged_username = self.request.user.username
        user = User.objects.get(username=logged_username)
        try:
            data = MediaUpload.objects.get(user=user)
        except:
            data = None
        return render(request, "app1/viewprofile.html", {"data": data, "user": user})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().dispatch(request, *args, **kwargs)
    
class ViewProfileApi(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        logged_username = self.request.user.username
        user = User.objects.get(username=logged_username)
        try:
            data = MediaUpload.objects.get(user=user)
        except:
            data = None
        datas = MediaUploadSerializer(data)  #MediaUploadSerializer(data, many=True) --> many=True can only used when object has multiple data
        users = UserSerializer(user)
        print(users.data)
        return Response({"data": datas.data, "user": users.data})