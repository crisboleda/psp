
# Django
from django.db.models import Sum, F
from django.db.models.functions import Coalesce, Ceil


# ANALYSIS TOOLS
ANALYSIS_TOOLS = ["actual size", "defects removed", "defects injected", "total time", "failure cost of quality", "appraisal cost of quality", "total defects", "size estimation error", "actual development time", "time estimation error", "percent compile time", "percent test time", "percent compile + test time", "yield vs A/FR", "A/FR vs yield", "defect injection % by phase", "defect removal % by phase", "total cost of quality", "appraisal to failure ratio"]


TIME_TOTAL_BY_PROGRAM = Coalesce(Sum(Ceil(F('program_log_time__delta_time') / 60.0)), 0)
