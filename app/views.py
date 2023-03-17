from django.shortcuts import render
# from app.models import Employee
from rest_framework import status,serializers
from app.serializers import MeetingTimeSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime as dt
from datetime import datetime
from app.models import MeetingRoom,MeetingTime
# Create your views here.

class BookMeetingRoom(APIView):

    
        

    def get(self,request):
        return Response(status=status.HTTP_200_OK)
    

    def post(self,request):
        meeting  = MeetingTimeSerializer(data=request.data)

        '''
        Excluding buffer time
        '''

        buffer_time  = ['9:00', '13:15','18:45']
        if request.data['start_time'] in buffer_time:
            return Response("You cannot book during buffer time",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        date = request.data['date']
        start_time  = request.data['start_time']
        end_time = request.data['end_time']
        start_time_dt =datetime.strptime(start_time, '%H:%M').time()
        end_time_dt =datetime.strptime(end_time, '%H:%M').time()


        '''
        setting start and end time format
        '''

        time_format=['00','15','30','45']
        if start_time[3:5] not in time_format:
            return Response ("Please give a correct time format [xx:00,xx:15,xx:30,xx:45]",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        if end_time[3:5] not in time_format:
            return Response ("Please give a correct time format [xx:00,xx:15,xx:30,xx:45]",status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
        '''
        Booking rooms according to no of members
        '''
        if int(request.data['members'])<=3:
            request.data['meeting_room'] = 1
            if MeetingTime.objects.filter(date=date,start_time=start_time,meeting_room=1):
                request.data['meeting_room'] = 2
            if MeetingTime.objects.filter(date=date,start_time=start_time,meeting_room=2):
                request.data['meeting_room'] = 3
        elif int(request.data['members'])>3 and int(request.data['members']) <=7:
            request.data['meeting_room'] = 2
            if MeetingTime.objects.filter(date=date,start_time=start_time,meeting_room=2):
                request.data['meeting_room'] = 3
        else:
            request.data['meeting_room'] = 3



        '''
        blocking user to book the room during buffer time
        '''
        l=[]
        for i in buffer_time:
            z=datetime.strptime(i,'%H:%M').time()
            l.append(z)
        for i in l:
            if i >start_time_dt and i<end_time_dt:
                return Response("You cannot book if buffer time in betwwen",status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        '''
        Checking availability of meeting rooms
        '''

        meeting_time = MeetingTime.objects.filter(date = date ,start_time = start_time,meeting_room = request.data['meeting_room'])
        
        if meeting_time:
            
        
            return Response("All rooms are already booked",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

        
        



        '''Saving the meeting
        '''
        if meeting.is_valid():
            
            meeting.save()
            return Response("Booked successfully",status=status.HTTP_201_CREATED)
        return Response("Some error occured",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
	