
# Django


# Django REST Framework
from rest_framework import serializers

# Models
from users.models import Profile, ExperienceCompany, PositionCompany
from logs.models import Phase, DefectLog
from programs.models import Program


class ProfileExperencieSerializer(serializers.ModelSerializer):

    years_development = serializers.IntegerField(required=False, min_value=0, max_value=100)

    years_configuration = serializers.IntegerField(min_value=0, required=False, max_value=100)

    years_integration = serializers.IntegerField(min_value=0, required=False, max_value=100)

    years_requirements = serializers.IntegerField(min_value=0, required=False, max_value=100)

    years_design = serializers.IntegerField(min_value=0, required=False, max_value=100)

    years_tests = serializers.IntegerField(min_value=0, required=False, max_value=100)

    years_support = serializers.IntegerField(min_value=0, required=False, max_value=100)


    def validate_years_development(self, value):
        return self.validate_value_is_null(value)

    def validate_years_configuration(self, value):
        return self.validate_value_is_null(value)

    def validate_years_integration(self, value):
        return self.validate_value_is_null(value)

    def validate_years_requirements(self, value):
        return self.validate_value_is_null(value)

    def validate_years_design(self, value):
        return self.validate_value_is_null(value)

    def validate_years_tests(self, value):
        return self.validate_value_is_null(value)

    def validate_years_support(self, value):
        return self.validate_value_is_null(value)

    def validate_value_is_null(self, value):
        if value == None:
            return 0
        return value


    class Meta:
        model = Profile
        fields = ('years_development', 'years_configuration', 'years_integration', 'years_requirements', 'years_design', 'years_tests', 'years_support')



class PositionCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = PositionCompany
        fields = ('name', 'created_at', 'updated_at')


class ExperencieCompanyModelSerializer(serializers.ModelSerializer):

    position_company = PositionCompanySerializer()

    class Meta:
        model = ExperienceCompany
        fields = ('name_company', 'position_company', 'years_position')


class ExperencieCompanySerializer(serializers.Serializer):

    name_company = serializers.CharField(max_length=70)

    position_company = serializers.CharField(max_length=70)

    years_position = serializers.IntegerField(min_value=1, max_value=20000000)


    def validate_position_company(self, position_name):
        try:
            return PositionCompany.objects.get(name=position_name)
        except PositionCompany.DoesNotExist:
            raise serializers.ValidationError("The position doesn't exists")


    def save(self, experencie):
        data = self.validated_data

        experencie.name_company = data["name_company"]
        experencie.position_company = data["position_company"]
        experencie.years_position = data["years_position"]

        experencie.save()

        return experencie


class DefectLogProgramSerializer(serializers.ModelSerializer):

    class Meta:
        model = DefectLog
        fields = ('date', 'description', 'solution', 'created_at', 'updated_at')


class DefectsRemovedPhaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Phase
        fields = ('name', 'abbreviation')


class DataProgramAnalysisTools(serializers.ModelSerializer):

    get_defects = serializers.StringRelatedField(many=True)

    class Meta:
        model = Program
        fields = ('pk', 'name', 'description', 'language', 'get_defects')
