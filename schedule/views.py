from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json


from .models import User, Schedule, Event

days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]

# Create your views here.

#login, register

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "schedule/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "schedule/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "schedule/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        s = Schedule()
        s.save()
        try:
            user = User.objects.create_user(username, email, password, uschedule = s)
            user.save()
        except IntegrityError:
            return render(request, "schedule/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "schedule/register.html")

def index (request):
    return render(request, 'schedule/index.html')

def check_valid(request, e):
    day_array = request.user.uschedule.events.filter(day=e.day).order_by('time_start')
    if e.time_start >= e.time_end:
        return False
    
    for ed in day_array:
        if e.time_start > ed.time_start and e.time_start < ed.time_end:
            return False
        if e.time_end > ed.time_start and e.time_end < ed.time_end:
            return False
        if e.time_start == ed.time_start or e.time_end == ed.time_end:
            return False
    return True

@login_required
def edit(request):
    global days
    msg = ""
    if (request.method == "POST"):
        if (request.POST["h"][0] == "D"):
            divide = request.POST["h"].index("|")
            row = request.POST["h"][1:divide]
            col = request.POST["h"][divide+1:]
            day_array = list(request.user.uschedule.events.filter(day=row).order_by('time_start'))
            print(row, col)
            day_array[int(col)].delete()
        else:
            d_num = days.index(request.POST["day"])
            e = Event(day = d_num, time_start=datetime.strptime(request.POST["stime"], "%H:%M").time(), time_end=datetime.strptime(request.POST["etime"],"%H:%M").time(), title=request.POST["title"])
            if check_valid(request, e):
                e.save()
                request.user.uschedule.events.add(e)
            else:
                msg = "Invalid Time, Please Try Again"
    
    #create array
    e_array = [[] for i in range(7)]
    max = 5
    for i in range(0, 7):
        day_array = request.user.uschedule.events.filter(day=i).order_by('time_start')
        if (len(day_array) > max):
            max = len(day_array)
        for d in day_array:
            e_array[i].append(d.title + "<br>"+str(d.time_start))
    m = list([i for i in range(max)])
    return render(request, 'schedule/edit.html', {
                "events": json.dumps(e_array), "max": m, "days": days, "message":msg
            })