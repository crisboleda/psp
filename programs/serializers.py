
# Django REST Framework
from rest_framework import serializers

# Models
from programs.models import BasePart, ReusedPart, NewPart


class UpdateBaseProgramSerializer(serializers.ModelSerializer):

    lines_current_base = serializers.IntegerField(min_value=1)
    lines_planned_base = serializers.IntegerField(min_value=1)

    class Meta:
        model = BasePart
        fields = (
            'lines_current_base', 'lines_current_added', 'lines_current_edited', 'lines_current_deleted', 'lines_planned_base', 'lines_planned_added', 'lines_planned_edited', 'lines_planned_deleted'
        )

    def validate(self, data):
        print("Hello world")
        import pdb; pdb.set_trace()


class UpdateReusedPartSerializer(serializers.ModelSerializer):

    planned_lines = serializers.IntegerField(min_value=1)

    class Meta:
        model = ReusedPart
        fields = ('planned_lines', 'current_lines')