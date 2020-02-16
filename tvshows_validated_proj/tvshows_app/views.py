from django.shortcuts import render, redirect
from .models import Show
from django.contrib import messages

def index(request):
    return redirect("/shows")

def create_show(request):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))

    else:
        show_title = request.POST["title"]
        show_network = request.POST["network"]
        show_release_date = request.POST["release_date"]
        show_desc = request.POST["desc"]
        
        show = Show.objects.create(title=show_title, network=show_network, release_date=show_release_date, desc=show_desc)
        context = {
            "show": show,
        }
        url = f"/shows/{show.id}"
        return redirect(url)

def view_show(request, id):
    show = Show.objects.get(id=id)
    context = {
        "show": show,
    }
    return render(request, "show.html", context)

def all_shows(request):
    context = {
        "all_shows": Show.objects.all(),
    }
    return render(request, "index.html", context)

def new_show(request):
    return render(request, "new_show.html")

def edit_show(request, id):
    show = Show.objects.get(id=id)
    date = show.release_date.strftime("%Y-%m-%d")
    context = {
        "show": show,
        "date": date,
    }
    print("=================> edit_show show title: ", show.title)

    return render(request, "edit_show.html", context)

def update_show(request, id):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)

        # url = f"/shows/{id}/edit"
        # return redirect(url)

        # redirect to stay on same page
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        show = Show.objects.get(id = id)
        show.title = request.POST["title"]
        show.network = request.POST["network"]
        show.release_date = request.POST["release_date"]
        show.desc = request.POST["desc"]
        show.save()
        
        context = {
            "show": show,
        }
        url = f"/shows/{show.id}"
        return redirect(url)

def destroy_show(request, id):
    show = Show.objects.get(id = id)
    show.delete()
    return redirect("/")
