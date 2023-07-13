from rest_framework.serializers import ModelSerializer
from .models import Places, Bus, BusStatus, UserBooking, MediaUpload
from rest_framework import serializers
from django.contrib.auth.models import User

class PlacesSerializer(ModelSerializer):
    places = serializers.CharField(max_length=100)
    class Meta:
        model = Places
        fields = "__all__"


class BusSerializer(ModelSerializer):
    class Meta:
        model = Bus
        fields = "__all__"

class BusStatusSerializer(ModelSerializer):
    class Meta:
        model = BusStatus
        fields = "__all__"

class UserBookingSerializer(ModelSerializer):
    class Meta:
        model = UserBooking
        fields = "__all__"

###########  Except Models #################

class SignUpApiSerializer(serializers.Serializer):
    message = serializers.CharField(required=False)
    logged_username = serializers.CharField(required=False)
    logged_email = serializers.CharField(required=False)

class LogInApiSerializer(serializers.Serializer):
    message = serializers.CharField(required=False)
    logged_email = serializers.EmailField(required=False)


class MediaUploadSerializer(ModelSerializer):
    class Meta:
        model = MediaUpload
        fields = "__all__"

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"