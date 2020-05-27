
# Django REST Framework
from rest_framework import serializers

# Models
from programs.models import BasePart


class UpdateBaseProgramSerializer(serializers.ModelSerializer):

    lines_current_base = serializers.IntegerField(min_value=1)

    class Meta:
        model = BasePart
        fields = ('lines_current_base', 'lines_current_added', 'lines_current_edited', 'lines_current_deleted')
