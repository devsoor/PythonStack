from django.shortcuts import render, redirect
from .models import User, Message, Comment
from django.contrib import messages
import bcrypt
from datetime import date, datetime, timezone, timedelta
import pytz
import pprint

def index(request):
    return render(request, "index.html")

def register(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_pw = request.POST['confirm_pw']

        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(first_name=first_name, last_name=last_name, email=request.POST['email'], pw_hash=pw_hash)
        request.session["first_name"] = first_name
        request.session['user_email'] = email
        return redirect("/wall")

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
                return redirect("/wall")

        messages.error(request, "Password does not match")
        return redirect("/")

def logout(request):
    try:
        del request.session['first_name']
        del request.session['user_email']
        # or we could do a request.session.flush() as well
    except KeyError:
        pass
    return redirect("/")

def success(request):
    try:
        request.session["first_name"]
    except:
        return render(request, "invaliduser.html")

    context = {
        "first_name": request.session["first_name"]
    }
    return render(request, "success.html", context)

def time_pst(d):
    timezone = pytz.timezone("America/Los_Angeles")
    d = timezone.localize(d)
    return d

def wall(request):
    this_user = User.objects.get(email=request.session['user_email'])
    message_list = []
    all_messages = Message.objects.all().order_by("-created_at")

    context = {
        "first_name": this_user.first_name,
        "message_list": all_messages,
    }
    return render(request, "wall.html", context)

def post_message(request):
    message = request.POST["message"]
    this_user = User.objects.get(email=request.session['user_email'])
    Message.objects.create(message=message, user=this_user)
    return redirect("/wall")

def post_comment(request):
    comment = request.POST["comment"]
    message_id = request.POST["message_id"]
    this_user = User.objects.get(email=request.session['user_email'])

    # attach tis comment to the message using the message_id
    this_message = Message.objects.get(id=message_id)

    if this_user.email != this_message.user.email:
        Comment.objects.create(comment=comment, user=this_user, message=this_message)
    return redirect("/wall")

def message_delete(request):
    message_id = request.POST["message_id"]
    this_message = Message.objects.get(id=message_id)

    timeout = 30
    curr_time = datetime.now()
    time_delta = curr_time - this_message.created_at
    mins_delta = time_delta.seconds/60
    # print(f"time_delta = {curr_time} - {this_message.created_at} = {time_delta}, time_delta = {time_delta.seconds/60} mins")
    if this_message.user.email == request.session['user_email'] and mins_delta <= timeout:
        this_message.delete()
    return redirect("/wall")

