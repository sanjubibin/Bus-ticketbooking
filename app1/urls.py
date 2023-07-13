from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.LogIn.as_view(), name="login"),
    path("rest/login", views.LoginView.as_view(), name="rest_login"),

    path("signin", views.SignUp.as_view(), name="signin"),
    path("rest/signup", views.SignUpApi.as_view(), name="rest_signup"),

    path("auth", views.AdminPage.as_view(), name="adminpage"),
    path("auth/rest", views.AdminPageApi.as_view(), name="rest_adminpage"),

    path("auth/home", views.Home.as_view(), name="homepage"),
    path("auth/rest/home", views.HomeApi.as_view(), name="rest_homepage"),

    path("auth/checkavailability", views.CheckAvailability.as_view(), name="checkavailability"),
    path("auth/rest/checkavailability", views.CheckAvailabilityApi.as_view(), name="rest_checkavailability"),

    path("auth/bookticket", views.BookTicket.as_view(), name="bookticket"),
    path("auth/rest/bookticket", views.BookTicketApi.as_view(), name="rest_bookticket"),

    path("auth/send_mail", views.SendMail.as_view(), name="confirmmail"),

    path("auth/filteruser", views.FilterUser.as_view(), name="filteruser"),
    path("auth/rest/filteruser", views.FilterUserApi.as_view(), name="rest_filteruser"),

    path("auth/addplace", views.PlaceAdd.as_view(), name="addplace"),
    path("auth/rest/addplace", views.PlaceAddApi.as_view(), name="rest_addplace"),

    path("auth/editplace", views.PlaceEdit.as_view(), name="editplace"),
    path("auth/rest/editplace", views.PlaceEditApi.as_view(), name="rest_editplace"),

    path("auth/deleteplace", views.PlaceDelete.as_view(), name="deleteplace"),
    path("auth/rest/deleteplace", views.PlaceDeleteApi.as_view(), name="rest_deleteplace"),

    path("auth/addbus", views.BusAdd.as_view(), name="addbus"),
    path("auth/rest/addbus", views.BusAddApi.as_view(), name="rest_addbus"),

    path("auth/editbus", views.BusEdit.as_view(), name="editbus"),
    path("auth/rest/editbus", views.BusEditApi.as_view(), name="rest_editbus"),

    path("auth/deletebus", views.BusDelete.as_view(), name="deletebus"),
    path("auth/rest/deletebus", views.BusDeleteApi.as_view(), name="rest_deletebus"),

    path("auth/addbusstatus", views.BusStatusAdd.as_view(), name="addbusstatus"),
    path("auth/rest/addbusstatus", views.BusStatusAddApi.as_view(), name="rest_addbusstatus"),

    path("auth/home/userdetails", views.UserBookingDetails.as_view(), name="userdetail"),
    path("auth/rest/home/userdetails", views.UserBookingDetailsApi.as_view(), name="rest_userdetail"),

    path("logout", views.LogOutSite.as_view(), name="logout"),
    # path("rest/logout", views.LogoutView.as_view(), name="rest_logout"),
    path("rest/logout", views.LogoutView.as_view(), name="rest_logout"),

    path("auth/addprofile", views.EditProfileView.as_view(), name="Addprofile"),
    path("auth/rest/addprofile", views.EditProfileViewApi.as_view(), name="rest_Addprofile"),

    path("auth/viewprofile", views.ViewProfile.as_view(), name="viewprofile"),
    path("auth/rest/viewprofile", views.ViewProfileApi.as_view(), name="rest_viewprofile")
]