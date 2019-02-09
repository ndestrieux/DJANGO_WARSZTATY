from django.shortcuts import render, Http404
from .models import *


# Create your views here.

# Room

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


def del_room(request, room_id):
    try:
        room_to_delete = Room.objects.get(pk=room_id)
        name = f"{room_to_delete.name}"
        room_to_delete.delete()
        return render(request, "delete.html", {"name": name})
    except Room.DoesNotExist:
        raise Http404(f"Person with ID {room_id} does not exist")


def room_details(request, room_id):
    try:
        room = Room.objects.get(pk=room_id)
        return render(request, "room_details.html", {"room": room})
    except Room.DoesNotExist:
        raise Http404(f"Room with ID {room_id} does not exist")


def rooms(request):
    r = Room.objects.all()
    print(r)
    return render(request, "rooms.html", {"r": r})


def reservation(request):
    try:
        room_id = request.POST["book"]
        room = Room.objects.get(pk=room_id)
        return render(request, "reservation.html", {"room": room})
    except Room.DoesNotExist:
        raise Http404(f"Room with ID {room_id} does not exist")

