
# Django


# Django REST Framework
from rest_framework import serializers

# Models
from users.models import Profile


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