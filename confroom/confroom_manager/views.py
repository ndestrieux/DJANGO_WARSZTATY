from django.shortcuts import render, Http404
from django.db.models import Q
from datetime import datetime as dt
from .models import *


# Create your views here.

# Main page

def rooms(request):
    r = Room.objects.all()
    print(r)
    return render(request, "rooms.html", {"r": r})


# Create new room

def new_room(request):
    if request.method == "GET":
        return render(request, "new_room.html")
    elif request.method == "POST":
        try:
            # collecting data from form
            name = request.POST.get("name").title()
            capacity = request.POST.get("capacity")
            have_projector = request.POST.get("have_projector")
            # checking data
            if not (0 < len(name) and 0 < len(capacity)):
                raise ValueError("Name and capacity fields cannot be empty")
            have_projector = True if bool(have_projector) is True else False
            # creating new movie in DB
            new_entry = Room.objects.create(name=name, capacity=capacity, have_projector=have_projector)
            # updating many to many fields for new movie in DB
            return render(request, "new_room.html", {"message": f"Room {new_entry.name} added to database."})
        except ValueError as ve:
            return render(request, "new_room.html", {"message": ve})


# Update existing room

def modify_room(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        if request.method == "GET":
            return render(request, "modify_room.html", {"room": room})
        elif request.method == "POST":
            try:
                # collecting data from form
                name = request.POST.get("name").title()
                capacity = request.POST.get("capacity")
                have_projector = request.POST.get("have_projector")
                # checking data
                if not (0 < len(name) and 0 < len(capacity)):
                    raise ValueError("Name and capacity fields cannot be empty")
                have_projector = True if bool(have_projector) is True else False
                # creating new movie in DB
                Room.objects.filter(pk=room_id).update(name=name, capacity=capacity, have_projector=have_projector)
                room = Room.objects.get(pk=room_id)
                # updating many to many fields for new movie in DB
                return render(request, "modify_room.html", {"room": room, "message": f"Room {room.name} updated in database."})
            except ValueError as ve:
                return render(request, "modify_room.html", {"message": ve})
    except Room.DoesNotExist:
        raise Http404(f"Room with ID {room_id} does not exist")


# Delete room

def del_room(request, room_id):
    try:
        room_to_delete = Room.objects.get(pk=room_id)
        name = f"{room_to_delete.name}"
        room_to_delete.delete()
        return render(request, "delete.html", {"name": name})
    except Room.DoesNotExist:
        raise Http404(f"Person with ID {room_id} does not exist")


# Display room details

def room_details(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        return render(request, "room_details.html", {"room": room})
    except Room.DoesNotExist:
        raise Http404(f"Room with ID {room_id} does not exist")


# Make a reservation

def reservation(request):
        try:
            now = dt.now().strftime("%Y-%m-%d")
            if request.method == "GET":
                raise Http404("REQUEST METHOD ERROR: no room was chosen for reservation")
            elif request.method == "POST":
                if request.POST.get("book"):
                    room_id = request.POST["book"]
                    room = Room.objects.get(pk=room_id)
                    return render(request, "reservation.html", {"room": room, "now": now})
                elif request.POST.get("confirm"):
                    room_id = request.POST.get("room_id")
                    room = Room.objects.get(pk=room_id)
                    date = dt.strptime(request.POST.get("date"), "%Y-%m-%d")
                    comment = request.POST.get("comment")
                    print(date)
                    if Reservation.objects.filter(room=room, date=date).exists():
                        return render(request, "reservation.html",
                                      {"room": room, "now": now, "comment": comment, "error": True})
                    Reservation.objects.create(room=room, date=date, comment=comment)
                    return render(request, "reservation.html",
                                  {"room": room, "reservation_date": dt.strftime(date, "%A %-d, %B %Y")})
        except Room.DoesNotExist:
            raise Http404(f"Room with ID {room_id} does not exist")


# Search a room

def search(request):
    now = dt.now().strftime("%Y-%m-%d")
    if request.method == "GET":
        return render(request, "search_room.html", {"now": now})
    elif request.method == "POST":
        try:
            # collecting data from form
            name = request.POST.get("name")
            minimum_capacity = int(request.POST.get("minimum_capacity"))
            date = dt.strptime(request.POST.get("date"), "%Y-%m-%d")
            have_projector = bool(request.POST.get("have_projector"))
            print(name, minimum_capacity, date, have_projector)
            query = Q()
            # build search by title query if not empty
            if name is not "":
                query.add(Q(name__icontains=name), Q.AND)
            query.add(Q(capacity__gte=minimum_capacity), Q.AND)
            query.add(Q(have_projector=have_projector), Q.AND)
            search_result = Room.objects.filter(query).exclude(reservation__date__exact=date)
            return render(request, "search_room.html", {"search_result": search_result, "now": now,
                                                        "no_data": True if len(search_result) == 0 else False})
        except ValueError as ve:
            print(ve)
            return render(request, "search_room.html")
