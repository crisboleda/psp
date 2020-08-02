
# Django REST Framework
from rest_framework import serializers

# Models
from programs.models import BasePart, ReusedPart, NewPart, Estimation, TypePart, SizeEstimation, Report, Pip


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


class UpdateNewPartSerializer(serializers.Serializer):

    name_part = serializers.CharField(max_length=150)

    type_part = serializers.CharField(max_length=30)

    size_estimation = serializers.CharField(max_length=2)

    planning_methods = serializers.IntegerField(max_value=2000000000, min_value=1)

    current_methods = serializers.IntegerField(max_value=2000000000, min_value=0, required=False)
    current_lines = serializers.IntegerField(max_value=2000000000, min_value=0, required=False)


    def validate_type_part(self, type_part):
        try:
            return TypePart.objects.get(name=type_part)
        except TypePart.DoesNotExist:
            raise serializers.ValidationError("The type part doesn't exists")
    
    
    def validate_current_methods(self, current_methods):
        if current_methods == None:
            return 0
        return current_methods

    
    def validate_current_lines(self, current_lines):
        if current_lines == None:
            return 0
        return current_lines

    
    def validate_size_estimation(self, size_estimation):
        try:
            return SizeEstimation.objects.get(name=size_estimation)
        except SizeEstimation.DoesNotExist:
            raise serializers.ValidationError("The size estimation doesn't exists")


    def validate(self, data):
        try:
            self.estimation = Estimation.objects.get(type_part=data['type_part'], size_estimation=data['size_estimation'])
            self.planning_lines = data['planning_methods'] * self.estimation.lines_of_code
        except Estimation.DoesNotExist:
            raise serializers.ValidationError("The estimation doesn't exists")

        return data

    def save(self, part):
        data = self.validated_data
        
        part.name = data['name_part']
        part.estimation = self.estimation
        part.planning_methods = data['planning_methods']
        part.planning_lines = self.planning_lines
        part.current_methods = data['current_methods']
        part.current_lines = data['current_lines']

        part.save()

        return part


class NewPartModelSerializer(serializers.ModelSerializer):

    estimation = EstimationModelSerializer()

    class Meta:
        model = NewPart
        fields = ('name', 'estimation', 'planning_methods', 'planning_lines', 'current_methods', 'current_lines')



class ReportModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Report
        fields = ('name', 'date', 'objetive', 'description', 'conditions', 'expect_results', 'current_results')
        


class PIPModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pip
        fields = ('name', 'date', 'problems', 'proposal', 'comment')


