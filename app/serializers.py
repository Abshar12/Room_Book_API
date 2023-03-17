from rest_framework import serializers
from app.models import MeetingTime

class MeetingTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingTime
        fields = "__all__"
    
