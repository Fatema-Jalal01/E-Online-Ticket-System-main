from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Bus(models.Model):
    bus_name=models.CharField(max_length=250,null=True)
    bus_id = models.CharField(max_length=250,null=True)
    total_seats = models.PositiveIntegerField(default=0)
    busfrom=models.CharField(max_length=250,null=True)
    busto=models.CharField(max_length=250,null=True)
    fare = models.IntegerField(null=True)
    busEstimation=models.CharField(max_length=250,null=True)
    busdate = models.DateField(null=True)
    
class Air(models.Model):
    air_name=models.CharField(max_length=250,null=True)
    air_id = models.CharField(max_length=250,null=True)
    airfrom=models.CharField(max_length=250,null=True)
    airto=models.CharField(max_length=250,null=True)
    AirEstimation=models.CharField(max_length=250,null=True)
    afair = models.IntegerField(null=True)
    airdate = models.DateField(null=True)
    
class Train(models.Model):
    t_name=models.CharField(max_length=250,null=True)
    train_id = models.CharField(max_length=250,null=True)
    t_class = models.CharField(max_length=250,null=True)
    tfrom=models.CharField(max_length=250,null=True)
    tto=models.CharField(max_length=250,null=True)
    tfare = models.CharField(max_length=250,null=True)
    tEstimation=models.CharField(max_length=250,null=True)
    traindate = models.DateField(null=True)

class userinfo(models.Model):
    username = models.CharField(max_length=20,null=True)

class Bususer(models.Model):
    name = models.ForeignKey(userinfo, on_delete=models.CASCADE,null=True)
    businfo = models.ForeignKey(Bus, on_delete=models.CASCADE,null=True)

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,null=True)
    seat_number = models.CharField(max_length=22,null=True)
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Trainseat(models.Model):
    train = models.ForeignKey(Train, on_delete=models.CASCADE,null=True)
    seat_number = models.CharField(max_length=22,null=True)
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class Planeseat(models.Model):
    plane = models.ForeignKey(Air, on_delete=models.CASCADE,null=True)
    seat_number = models.CharField(max_length=22,null=True)
    is_booked = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

class bus_payment(models.Model):
    nid = models.CharField(max_length=22,null=True)
    gender = models.CharField(max_length=22,null=True)
    pay_method = models.CharField(max_length=22,null=True)
    number = models.CharField(max_length=22,null=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, null=True)


class train_payment(models.Model):
    nid = models.CharField(max_length=22,null=True)
    gender = models.CharField(max_length=22,null=True)
    pay_method = models.CharField(max_length=22,null=True)
    number = models.CharField(max_length=22,null=True)
    train = models.ForeignKey(Train, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    seat = models.ForeignKey(Trainseat, on_delete=models.CASCADE, null=True)

class air_payment(models.Model):
    nid = models.CharField(max_length=22,null=True)
    gender = models.CharField(max_length=22,null=True)
    pay_method = models.CharField(max_length=22,null=True)
    number = models.CharField(max_length=22,null=True)
    air = models.ForeignKey(Air, on_delete=models.CASCADE,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    seat = models.ForeignKey(Planeseat, on_delete=models.CASCADE, null=True)



class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nid = models.CharField(max_length=250,null=True)
    gender = models.CharField(
        max_length=6,
        choices=[('Male','Male'),('FeMale','FeMale')]
    )

    def __str__(self):
        return self.user.username