from django.contrib import admin
from django.urls import path
from res_app.views import AddRoom, ModifyRoom, delete_room, show_room, RoomReservation, Main

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Main.as_view(), name='main'),
    path('<id_rooms>', Main.as_view(), name='main'),
    path('room/new', AddRoom.as_view(), name='add_room'),
    path('room/modify/<int:id>', ModifyRoom.as_view(), name='modify_room'),
    path('room/delete/<int:id>', delete_room, name='delete_room'),
    path('room/<int:id>', show_room, name='show_room'),
    # path('allrooms', show_all_rooms, name='show_all_rooms'),
    # path('reservation', AddReservation.as_view(), name='add_reservation'),
    path('reservation/<int:room_id>', RoomReservation.as_view(), name='room_reservation')
]
