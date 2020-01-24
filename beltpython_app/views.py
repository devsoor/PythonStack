from django.shortcuts import render, redirect
from .models import User, Trip
from django.contrib import messages
import bcrypt
from datetime import date, datetime, timezone, timedelta
import pytz
import pprint
from django.db.models import Q


def index(request):
    return render(request, "login.html")

def register_user(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        level = "normal"
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_pw = request.POST['confirm_pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        this_user = User.objects.filter(email=email)
        if len(this_user) != 0:
            return redirect("/")

        if User.objects.exists() == False:
            level = "admin"
            print("setting admin level")

        if len(User.objects.filter(email=email)) == 0 and level != "admin":
            level = "normal"
            print("setting normal level")

        User.objects.create(first_name=first_name, last_name=last_name, email=request.POST['email'], pw_hash=pw_hash, level=level)
        request.session["first_name"] = first_name
        request.session['user_email'] = email
        return redirect("/dashboard")

def signin(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.filter(email=email)
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(password.encode(), logged_user.pw_hash.encode()):
                request.session['user_email'] = logged_user.email
                request.session["first_name"] = logged_user.first_name
                return redirect("/dashboard")

        messages.error(request, "Password does not match")
        return redirect("/")

def logout(request):
    try:
        request.session.clear()
    except KeyError:
        print("Exception: ")
        pass
    return redirect("/")

def dashboard(request):
    this_user = User.objects.get(email=request.session['user_email'])
    trip_list = Trip.objects.filter(user=this_user)
    other_trips = Trip.objects.all().exclude(creator=this_user)

    
    context = {
        "this_user": this_user,
        "trip_list": trip_list,
        # "other_trips": other_trips,
    }
    return render(request, "dashboard.html", context)

def view_trip(request, id):
    context = {
        "this_trip": Trip.objects.get(id=id),
        "first_name": request.session['first_name'],

    }
    this_trip = Trip.objects.get(id=id)

    return render(request, "view_trip.html", context)

def new_trip(request):
    return render(request, "new_trip.html")

def create_trip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        destination = request.POST["destination"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        plan = request.POST["plan"]
        creator = User.objects.get(email=request.session['user_email'])

        trip = Trip.objects.create(destination=destination, start_date=start_date, end_date=end_date, plan=plan, creator=creator)

    return redirect("/dashboard")

def edit_form(request, id):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        this_trip = Trip.objects.get(id=id)
        this_trip.destination = request.POST["destination"]
        this_trip.start_date = request.POST["start_date"]
        this_trip.end_date = request.POST["end_date"]
        this_trip.plan = request.POST["plan"]
        this_trip.save()
    return redirect("/dashboard")


def edit_trip(request, id):
    this_trip = Trip.objects.get(id=id)

    start_date = this_trip.start_date.strftime("%Y-%m-%d")
    end_date = this_trip.end_date.strftime("%Y-%m-%d")

    context = {
        "this_trip": this_trip,
        "start_date": start_date,
        "end_date": end_date,
        "first_name": request.session['first_name'],
    }
    return render(request, "edit_trip.html", context)

def remove_trip(request, id):
    this_trip = Trip.objects.get(id=id)
    this_trip.delete()
    return redirect("/dashboard")

def join_trip(request, id):
    user_join = request.POST["user_join"]
    new_user = User.objects.get(id=user_join)
    print("====> user_join is : ", user_join)
    print("====> trip id is : ", id)
    this_trip = Trip.objects.get(id=id)
    this_user = User.objects.get(email=request.session['user_email'])

    print("this trip to cancel and join other is:", this_trip.destination)
    print("this_user: ", this_user.first_name)

    x = Trip.objects.filter(user=this_user)
    print("xxxxx ", x)
    for i in x:
        print("------> destination = ", i.destination)
    this_user.trip.add(this_trip)

    this_trip.save()


    new_user.trip.remove(this_trip)
    new_user.save()

    return redirect("/dashboard")