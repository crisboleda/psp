
# Django REST Framework
from rest_framework import serializers

# Models
from logs.models import TimeLog


class UpdateTimeLogModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeLog
        fields = ('delta_time', 'is_paused')