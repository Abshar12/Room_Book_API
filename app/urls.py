from django.urls import path
from app.views import BookMeetingRoom

urlpatterns=[
    path('book',BookMeetingRoom.as_view())
]