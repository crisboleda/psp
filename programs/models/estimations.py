
# Django
from django.db import models


# (VS, S, M, L, X)
class SizeEstimation(models.Model):
    name = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

# (Logic, I/O)
class TypePart(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Estimation(models.Model):
    type_part = models.ForeignKey(TypePart, on_delete=models.CASCADE, related_name='estimation_proxy')
    size_estimation = models.ForeignKey(SizeEstimation, on_delete=models.CASCADE, related_name='size_estimation_proxy')
    lines_of_code = models.DecimalField(null=False, blank=False, max_digits=6, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Type part '{}' - Size estimation {} - lines of code {}".format(self.type_part, self.size_estimation, self.lines_of_code)
    