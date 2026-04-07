from django.urls import path
from . import views

app_name = "platform2"

urlpatterns = [
    path("", views.home, name="home"),
    path("submit/", views.submit, name="submit"),
    path("room/", views.room_join, name="room_join"),
    path("board/", views.board, name="board"),
    path("board/add/challenge/", views.board_add_challenge, name="board_add_challenge"),
    path("board/add/idea/", views.board_add_idea, name="board_add_idea"),
    path("board/layout/<int:pk>/", views.update_layout, name="update_layout"),
    path("board/check/<int:pk>/", views.toggle_check, name="toggle_check"),
    path("board/delete/<int:pk>/", views.board_delete, name="board_delete"),
    path("board/approve/<int:pk>/", views.board_approve, name="board_approve"),
]