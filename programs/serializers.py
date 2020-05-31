
# Django REST Framework
from rest_framework import serializers

# Models
from programs.models import BasePart, ReusedPart, NewPart, Estimation, TypePart, SizeEstimation


class UpdateBaseProgramSerializer(serializers.ModelSerializer):

    lines_current_base = serializers.IntegerField(min_value=0, max_value=2000000000)
    lines_current_added = serializers.IntegerField(min_value=0, max_value=2000000000)
    lines_current_edited = serializers.IntegerField(min_value=0, max_value=2000000000)
    lines_current_deleted = serializers.IntegerField(min_value=0, max_value=2000000000)

    lines_planned_base = serializers.IntegerField(min_value=1, max_value=2000000000)
    lines_planned_added = serializers.IntegerField(min_value=0, max_value=2000000000)
    lines_planned_edited = serializers.IntegerField(min_value=0, max_value=2000000000)
    lines_planned_deleted = serializers.IntegerField(min_value=0, max_value=2000000000)

    class Meta:
        model = BasePart
        fields = (
            'lines_current_base', 'lines_current_added', 'lines_current_edited', 'lines_current_deleted', 'lines_planned_base', 'lines_planned_added', 'lines_planned_edited', 'lines_planned_deleted'
        )

    def validate(self, data):
        self.validate_lines(
            data['lines_planned_base'],
            data['lines_planned_edited'],
            data['lines_planned_deleted']
        )
        
        self.validate_lines(
            data['lines_current_base'],
            data['lines_current_edited'],
            data['lines_current_deleted']
        )

        return data

    def validate_lines(self, base_lines, edited_lines, deleted_lines):
        if base_lines < deleted_lines or edited_lines > (base_lines - deleted_lines):
            raise serializers.ValidationError("The base lines doesn't enogth")


class UpdateReusedPartSerializer(serializers.ModelSerializer):

    planned_lines = serializers.IntegerField(min_value=1)

    class Meta:
        model = ReusedPart
        fields = ('planned_lines', 'current_lines')


class TypePartModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TypePart
        fields = ('pk', 'name', 'description')


class SizeEstimationModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SizeEstimation
        fields = ('pk', 'name', 'description')


class EstimationModelSerializer(serializers.ModelSerializer):

    type_part = TypePartModelSerializer()
    size_estimation = SizeEstimationModelSerializer()

    class Meta:
        model = Estimation
        fields = ('type_part', 'size_estimation', 'lines_of_code', 'created_at', 'updated_at')