from django.shortcuts import render
from .forms import AddRoomForm
from django.views import View
from django.shortcuts import redirect
from django.urls import reverse
from .models import Room, Reservation
from django.http import HttpResponse
import datetime
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


class Main(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Main, self).dispatch(request, *args, **kwargs)

    def get(self, request, id_rooms='all'):

        room_id = []

        if id_rooms == 'all':
            rooms = Room.objects.all()
        else:
            rooooms = id_rooms[0:-1].split(',')
            for room in rooooms:
                if room != 'favicon.ic':
                    room_id.append(int(room))
            rooms = Room.objects.filter(pk__in=room_id)
        today = datetime.date.today()
        page = '<center><h2>Hello!</h2></center><br>'
        page += '<h3>Search room</h3>'
        page += '''<form method="POST">
        <label>Room name<label><input type="text" name="name" /><br>
        <label>Minimum capacity<label><input type="number" step="1" min="1" name="capacity" /><br>
        <label>Free at day<label><input type="date" name="date" /><br>
        <label>Projector needed<label> <select>
        <option value="True">Yes</option>
        <option value="False">No</option>
        </select><br><input type="submit" value="Search" /></form><br><br> '''
        if id_rooms == 'all':
            page += '<h3>Status for all rooms:</h3><br>'
        else:
            page += '<h3>Status for searching rooms:</h3><br>'
        num = 1

        for room in rooms:
            page +=f"{num}. Name: <a href='http://127.0.0.1:8000/room/{room.id}' style=\"text-decoration: none\"> {room.name}</a>" \
                f"&emsp;&emsp;&emsp;<a href='http://127.0.0.1:8000/room/modify/{room.id}' style=\"text-decoration: none\">Modify</a>" \
                f"&emsp;<a href='http://127.0.0.1:8000/room/delete/{room.id}' style=\"text-decoration: none\">Delete</a><br>"
            page +=f"Today: "

            if Reservation.objects.filter(room=room, date=today):
                page += 'reserved<br><br>'
            else:
                page += 'free<br><br>'
            num += 1
        page += '<br><br><form method="GET" action="http://127.0.0.1:8000/room/new"><input type="submit" value="Add room" /></form>'

        return HttpResponse(page)

    def post(self, request, id_rooms=1):
        today = datetime.date.today()
        rooms = Room.objects.all()
        rom_id = []
        for room in rooms:
            rom_id.append(int(room.id))

        if request.POST.get('date'):

            if today > datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date():
                return HttpResponse('You are searching in past<br><br><form method="GET" '
                                    'action="http://127.0.0.1:8000/home"><input type="submit" value="Home" /></form>')
            date = request.POST.get('date')
            reservations = Reservation.objects.filter(date=date)
            res_id = []
            for reservation in reservations:
                res_id.append(int(reservation.room.id))
            print(res_id)
            print(rom_id)
            result = [x for x in rom_id if x not in res_id]
            print(result)

            rooms = rooms.filter(pk__in=result)

        if request.POST.get('name'):
            name = request.POST.get('name')
            rooms = rooms.filter(name__contains=name)

        if request.POST.get('capacity'):
            capacity = request.POST.get('capacity')
            rooms = rooms.filter(capacity__gte=capacity)

        if request.POST.get('projector') == 'true':
            rooms = rooms.filter(projector=True)

        id_rooms = ''

        for room in rooms:

            id_rooms +=str(room.id)+','

        return redirect(reverse('main', kwargs={'id_rooms': id_rooms}))


class AddRoom(View):

    def get(self, request):
        form = AddRoomForm()
        return render(request, 'add_room.html', {'form': form})

    def post(self, request):
        form = AddRoomForm(request.POST)
        form.save()
        return redirect(reverse('main'))


class ModifyRoom(View):

    def get(self, request, id):
        room = Room.objects.get(pk=id)
        return render(request, 'edit_room.html', {'room': room})

    def post(self, request, id):
        room = Room.objects.get(pk=id)
        room.name = request.POST.get('name')
        room.capacity = int(request.POST.get('capacity'))
        if request.POST.get('projector') == 'on':
            room.projector = True
        else:
            room.projector = False
        room.save()
        return redirect(reverse('main'))


def delete_room(request, id):
    room = Room.objects.get(pk=id)
    room.delete()
    return redirect(reverse('main'))


def show_room(request, id):

    today = datetime.date.today()
    room = Room.objects.get(pk=id)
    reservations = Reservation.objects.filter(room=room).order_by('date')
    return render(request, 'show_room.html', {'room': room, 'reservations': reservations, 'today': today})


class RoomReservation(View):

    def get(self, request, room_id):
        room = Room.objects.get(pk=room_id)
        return render(request, 'make_reservation.html', {'room': room})

    def post(self, request, room_id):
        book_day = datetime.datetime.strptime(request.POST.get('date'), '%Y-%m-%d').date()
        try:
            if datetime.date.today() <= book_day:
                date = request.POST.get('date')
                room = Room.objects.get(pk=room_id)
                comment = request.POST.get('comment')
                Reservation.objects.create(date=date, room=room, comment=comment)
                return HttpResponse('The reservation was successful<br><br><form method="GET" '
                                    'action="http://127.0.0.1:8000"><input type="submit" value="Home" /></form>')
            else:
                return HttpResponse('You can\'t make reservation on past<br><br><form method="GET" '
                                    'action="http://127.0.0.1:8000"><input type="submit" value="Home" /></form>')

        except IntegrityError:
            return HttpResponse(f"We sorry, but {room.name} is already booked on {date}.")
