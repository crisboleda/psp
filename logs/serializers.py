
# Django REST Framework
from rest_framework import serializers

# Models
from logs.models import TimeLog, Phase


class UpdateTimeLogModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeLog
        fields = ('delta_time', 'is_paused')


class TimeLogModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeLog
        fields = ('delta_time', 'start_date', 'finish_date', 'last_restart_time')


class CreateTimeLogModelSerializer(serializers.Serializer):

    name_phase = serializers.CharField(max_length=20)
    comments = serializers.CharField(max_length=100)

    def validate(self, data):
        try:
            self.phase = Phase.objects.get(name=data['name_phase'])
        except Phase.DoesNotExist:
            serializers.ValidationError("The phase doesn't exists")

        return data


    def save(self, program):
        data = self.validated_data
        return TimeLog.objects.create(phase=self.phase, program=program, comments=data['comments'])