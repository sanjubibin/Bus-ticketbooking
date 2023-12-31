# Generated by Django 4.2.2 on 2023-07-06 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_no', models.CharField(max_length=20, unique=True)),
                ('bus_name', models.CharField(max_length=50, unique=True)),
                ('total_seats', models.IntegerField()),
                ('bus_type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='BusStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_available', models.IntegerField()),
                ('start_date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_date', models.DateField()),
                ('end_time', models.TimeField()),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.bus')),
            ],
        ),
        migrations.CreateModel(
            name='Places',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('places', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booked_date', models.DateField()),
                ('booked_time', models.TimeField()),
                ('no_of_seats', models.IntegerField()),
                ('user_pickup_point', models.CharField(max_length=200)),
                ('user_dropdown_point', models.CharField(max_length=200)),
                ('user_pickup_date', models.DateField()),
                ('user_pickup_time', models.TimeField()),
                ('user_dropdown_date', models.DateField()),
                ('user_dropdown_time', models.TimeField()),
                ('busstatus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app1.busstatus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MediaUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='images')),
                ('address', models.CharField(max_length=300)),
                ('mobile', models.CharField(max_length=10, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='busstatus',
            name='end_place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_ending_place', to='app1.places'),
        ),
        migrations.AddField(
            model_name='busstatus',
            name='start_place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_starting_place', to='app1.places'),
        ),
    ]
