from django.db import models

# Create your models here.


class MeetingRoom(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.IntegerField()

class MeetingTime(models.Model):
    date = models.DateField(auto_now=False,auto_now_add=False)
    start_time = models.TimeField(default=None)
    end_time = models.TimeField(default=None)
    members = models.IntegerField()
    meeting_room = models.ForeignKey(MeetingRoom,on_delete=models.CASCADE)