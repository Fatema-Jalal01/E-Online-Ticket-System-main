#from django.http import HttpResponse
from django.shortcuts import render,HttpResponse,redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from service.models import Bus,Air,Train,userinfo,Seat,Trainseat,Planeseat,bus_payment,train_payment,air_payment
from django.contrib import messages
from django.template import loader
from django.db.models import Count
from django.core.exceptions import ValidationError

from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='login')
def homepage(request):
    return render(request,"home.html")

def loginpage(request):

    if request.method == "POST" :
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')

        user = authenticate(request,username=username,password=pass1)

        if user is not None:
            mydata = userinfo(username=username)
            mydata.save()
            login(request,user)
            return redirect('homey')
        else:
            return HttpResponse("Your username or password is not valid!!!")
        
    return render(request,"login.html")

def term(request):
    return render(request,"term.html")

def signuppage(request):
    if request.method == "POST":
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists!")
            
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists!")
        
        if pass1!=pass2:
            return HttpResponse("Your password and confirm password both are not same!!!")
        else:
            my_user = User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')

        

    return render(request,"sign.html")

def homey(request):
    return render(request,"homepage1.html")

def logoutpage(request):
    logout(request)
    return redirect('login')


def bus(request):

    if request.method == "POST":
        bus_obj = Bus.objects.all()
        frm = request.POST.get('from')
        to = request.POST.get('to')
        date = request.POST.get('date')
        mydata = Bus.objects.filter(busfrom=frm,busto=to,busdate__exact = date).values()
        
        if mydata is not None:
            template = loader.get_template('searchbus.html')
            context = {
                'bus_obj': mydata,
            }
        return HttpResponse(template.render(context, request))
    return render(request,"buspage.html")



def train(request):

    if request.method == "POST":
        bus_obj = Train.objects.all()
        frm = request.POST.get('from')
        to = request.POST.get('to')
        tclass = request.POST.get('Choose_a_class')
        date = request.POST.get('date')
        mydata = Train.objects.filter(tfrom=frm,tto=to,t_class=tclass,traindate__exact = date).values()

        if mydata is not None:
            template = loader.get_template('seracht.html')
            context = {
                'bus_obj': mydata,
            }
        return HttpResponse(template.render(context, request))
    return render(request,"train page.html")


def airplane(request):
    if request.method == "POST":
        air_obj = Air.objects.all()
        frma = request.POST.get('from')
        toa = request.POST.get('to')
        datea = request.POST.get('date')
        #Choose = request.POST.get('Choose a class')
        mydataa = Air.objects.filter(airfrom=frma,airto=toa,airdate__exact = datea).values()

        if mydataa is not None:
            template = loader.get_template('serachair.html')
            context = {
                'air_obj': mydataa,
            }
        return HttpResponse(template.render(context, request))
    return render(request,"Airplane.html")



@login_required    
def seat_selection(request,bus_id):

    current_user = request.user
    user_id = current_user.id
    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)
    #print(user_id)
    context = {'user_name' : user_name}

    bus = Bus.objects.get(bus_id=bus_id)
    seats = Seat.objects.filter(bus=bus)
    

    seat_exists = {}
    for i in range(1, 41):
        seat_exists[i] = Seat.objects.filter(bus=bus, seat_number=i).exists()

    if request.method == 'POST':
        seat_ids = request.POST.getlist('seat_id')
        for seat_id in seat_ids:
            if Seat.objects.filter(bus=bus, seat_number=seat_id, is_booked=True).exists():
                return HttpResponse("Seat has booked!!!")
            else:
                seat = Seat.objects.create(bus=bus, seat_number=seat_id, is_booked=True,user_id=user_id)
                seat.save()
        return redirect('buspay', bus_id=bus_id)
    return render(request, "seat_booking.html", {"seat_exists": seat_exists,'bus': bus, 'seats': seats,'bus_id': bus_id})

@login_required
def confirm(request):

    current_user = request.user
    current_user_id = current_user.id

    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    print(current_user_id)

    # Retrieve all the booked seats for the current user
    booked_seats = Seat.objects.filter(user=current_user, is_booked=True)
    bus_ids = [Seat.seat_number for Seat in booked_seats]
    buses = Bus.objects.filter(bus_id=bus_ids).distinct()
    
    context = {
        'booked_seats': booked_seats,
        'current_user_id' : current_user_id,
        'user_name' : user_name,
        'email' : email,
        'buses': buses,
       
    }

    return render(request, 'confirmation.html', context)


@login_required
def delete_seat(request):
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        try:
            seat = Seat.objects.get(seat_number=seat_id, user=request.user)
            seat.delete()
        except Seat.DoesNotExist:
            pass

    return redirect('confirm')



@login_required
def buspay(request,bus_id):

    current_user = request.user
    user_id = current_user.id
    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    bus = Bus.objects.get(bus_id=bus_id)

    if request.method == "POST":
        nid = request.POST.get('nid')
        gender = request.POST.get('gender')
        pay_method = request.POST.get('payment')
        number = request.POST.get('number')

        mydata1 = bus_payment.objects.create(bus=bus,nid=nid,gender=gender,pay_method = pay_method,number=number, user_id=user_id)
        mydata1.save()
        mydata = bus_payment.objects.filter(bus=bus,nid=nid,gender=gender,pay_method = pay_method,number=number).values
        return redirect('pay_temp', bus_id=bus_id)
        '''mydata = bus_payment.objects.filter(bus=bus,nid=nid,gender=gender,pay_method = pay_method,number=number).values
        if mydata is not None:
            template = loader.get_template('bus_pay_template.html',bus_id=bus_id)
            context = {

                'book': mydata,
            }
        return HttpResponse(template.render(context, request))'''
    return render(request,"new.html",{'user_name' : user_name, 'email' : email})

@login_required
def pay_temp(request, bus_id):

    current_user = request.user
    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    current_user_id = current_user.id

    print(current_user_id)
    # Retrieve the selected train from the database
    bus = Bus.objects.get(bus_id=bus_id)
    seat = Seat.objects.get
    # Retrieve all the booked seats for the selected train and current user
    # current_user_id = request.user.id
    booked_seats = Seat.objects.filter(bus=bus, is_booked=True,  user_id=current_user_id)
    booked = bus_payment.objects.filter(bus=bus, user_id=current_user_id)
    context = {
        'bus': bus,
        'booked_seats': booked_seats,
        'user_name' : user_name,
        'user_id' : current_user_id,
        'booked' :booked,
        'email' : email
    }
    return render(request,"bus_pay_template.html",context)


@login_required
def train_seat_selection(request, train_id):
    current_user = request.user
    user_id = current_user.id
    user_name = current_user.username
    email = current_user.email
    #print(user_name)
    #print(email)
    #print(user_id)
    context = {'user_name' : user_name}

    train = Train.objects.get(train_id=train_id)
    seats = Trainseat.objects.filter(train=train)

    seat_exists = {}
    for i in range(1, 41):
        seat_exists[i] = Trainseat.objects.filter(train=train, seat_number=i).exists()

    if request.method == 'POST':
        seat_ids = request.POST.getlist('seat_id')
        for seat_id in seat_ids:
            if Trainseat.objects.filter(train=train, seat_number=seat_id, is_booked=True).exists():
                return HttpResponse("Seat has booked!!!")
            else:
                seat = Trainseat.objects.create(train=train, seat_number=seat_id, is_booked=True, user_id=user_id)
                seat.save()
        return redirect('trainpay', train_id=train_id)

    return render(request, "train_seat_booking.html", {"seat_exists": seat_exists,'train': train, 'seats': seats,'train_id': train_id,'user_name' : user_name, 'email' : email})


@login_required
def train_confirm(request):


    current_user = request.user
    current_user_id = current_user.id

    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    print(current_user_id)

    # Retrieve all the booked seats for the current user
    booked_seats = Trainseat.objects.filter(user=current_user, is_booked=True)
    train_ids = [Trainseat.seat_number for Trainseat in booked_seats]
    trains = Train.objects.filter(train_id=train_ids).distinct()
    
    context = {
        'booked_seats': booked_seats,
        'current_user_id' : current_user_id,
        'user_name' : user_name,
        'email' : email,
        'trains': trains,
       
    }

    return render(request, 'train_seat_confirm.html', context)


@login_required
def train_delete_seat(request):
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        try:
            seat = Trainseat.objects.get(seat_number=seat_id, user=request.user)
            seat.delete()
        except Seat.DoesNotExist:
            pass

    return redirect('train_confirm')

@login_required
def trainpay(request,train_id):

    current_user = request.user
    user_id = current_user.id
    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    train = Train.objects.get(train_id=train_id)

    if request.method == "POST":
        nid = request.POST.get('nid')
        gender = request.POST.get('gender')
        pay_method = request.POST.get('payment')
        number = request.POST.get('number')

        mydata1 = train_payment.objects.create(train=train,nid=nid,gender=gender,pay_method = pay_method,number=number, user_id=user_id)
        mydata1.save()
        mydata = train_payment.objects.filter(train=train,nid=nid,gender=gender,pay_method = pay_method,number=number).values
        return redirect('train_pay_temp', train_id=train_id)
        '''mydata = bus_payment.objects.filter(bus=bus,nid=nid,gender=gender,pay_method = pay_method,number=number).values
        if mydata is not None:
            template = loader.get_template('bus_pay_template.html',bus_id=bus_id)
            context = {

                'book': mydata,
            }
        return HttpResponse(template.render(context, request))'''
    return render(request,"train_new.html",{'user_name' : user_name, 'email' : email})

@login_required
def train_pay_temp(request, train_id):

    current_user = request.user
    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    current_user_id = current_user.id

    print(current_user_id)
    # Retrieve the selected train from the database
    train = Train.objects.get(train_id=train_id)
    seat = Trainseat.objects.get
    # Retrieve all the booked seats for the selected train and current user
    # current_user_id = request.user.id
    booked_seats = Trainseat.objects.filter(train=train, is_booked=True,  user_id=current_user_id)
    booked = Trainseat.objects.filter(train=train, user_id=current_user_id)
    context = {
        'train': train,
        'booked_seats': booked_seats,
        'user_name' : user_name,
        'user_id' : current_user_id,
        'booked' :booked,
        'email' : email
    }
    return render(request,"train_pay_template.html",context)








@login_required
def plane_seat_selection(request, air_id):
    current_user = request.user
    user_id = current_user.id
    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)
    #print(user_id)
    context = {'user_name' : user_name}

    plane = Air.objects.get(air_id=air_id)
    seats = Planeseat.objects.filter(plane=plane)

    seat_exists = {}
    for i in range(1, 41):
        seat_exists[i] = Planeseat.objects.filter(plane=plane, seat_number=i).exists()

    if request.method == 'POST':
        seat_ids = request.POST.getlist('seat_id')
        for seat_id in seat_ids:
            if Planeseat.objects.filter(plane=plane, seat_number=seat_id, is_booked=True).exists():
                return HttpResponse("Seat has booked!!!")
            else:
                seat = Planeseat.objects.create(plane=plane, seat_number=seat_id, is_booked=True, user_id=user_id)
                seat.save()
        return redirect('planepay', air_id=air_id)

    return render(request, "plane_seat_booking.html", {"seat_exists": seat_exists,'plane': plane, 'seats': seats,'air_id': air_id,'user_name' : user_name, 'email' : email})


@login_required
def plane_confirm(request):

    current_user = request.user
    current_user_id = current_user.id

    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    print(current_user_id)

    # Retrieve all the booked seats for the current user
    booked_seats = Planeseat.objects.filter(user=current_user, is_booked=True)
    plane_ids = [Planeseat.seat_number for Planeseat in booked_seats]
    planes = Air.objects.filter(air_id=plane_ids).distinct()
    
    context = {
        'booked_seats': booked_seats,
        'current_user_id' : current_user_id,
        'user_name' : user_name,
        'email' : email,
        'planes': planes,
       
    }

    return render(request, 'plane_seat_confirm.html', context)


@login_required
def plane_delete_seat(request):
    if request.method == 'POST':
        seat_id = request.POST.get('seat_id')
        try:
            seat = Planeseat.objects.get(seat_number=seat_id, user=request.user)
            seat.delete()
        except Seat.DoesNotExist:
            pass

    return redirect('plane_confirm')



@login_required
def planepay(request,air_id):

    current_user = request.user
    user_id = current_user.id
    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    air = Air.objects.get(air_id=air_id)

    if request.method == "POST":
        nid = request.POST.get('nid')
        gender = request.POST.get('gender')
        pay_method = request.POST.get('payment')
        number = request.POST.get('number')

        mydata1 = air_payment.objects.create(air=air,nid=nid,gender=gender,pay_method = pay_method,number=number, user_id=user_id)
        mydata1.save()
        mydata = air_payment.objects.filter(air=air,nid=nid,gender=gender,pay_method = pay_method,number=number).values
        return redirect('plane_pay_temp', air_id=air_id)
        '''mydata = bus_payment.objects.filter(bus=bus,nid=nid,gender=gender,pay_method = pay_method,number=number).values
        if mydata is not None:
            template = loader.get_template('bus_pay_template.html',bus_id=bus_id)
            context = {

                'book': mydata,
            }
        return HttpResponse(template.render(context, request))'''
    return render(request,"air_new.html",{'user_name' : user_name, 'email' : email})

@login_required
def plane_pay_temp(request, air_id):

    current_user = request.user
    user_name = current_user.username
    email = current_user.email
    print(user_name)
    print(email)

    current_user_id = current_user.id

    print(current_user_id)
    # Retrieve the selected train from the database
    plane = Air.objects.get(air_id=air_id)
    seat = Planeseat.objects.get
    # Retrieve all the booked seats for the selected train and current user
    # current_user_id = request.user.id
    booked_seats = Planeseat.objects.filter(plane=plane, is_booked=True,  user_id=current_user_id)
    booked = Planeseat.objects.filter(plane=plane, user_id=current_user_id)
    context = {
        'plane': plane,
        'booked_seats': booked_seats,
        'user_name' : user_name,
        'user_id' : current_user_id,
        'booked' :booked,
        'email' : email
    }
    return render(request,"air_pay_template.html",context)


def term(request):
    return render(request,"Term&Policy.html")

def about(request):
    return render(request,"AboutUs.html")

def manual(request):
    return render(request,"manual.html")