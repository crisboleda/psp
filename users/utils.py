
# Django
from django.db.models import Sum, F
from django.db.models.functions import Coalesce, Ceil


# ANALYSIS TOOLS
ANALYSIS_TOOLS = ["actual size", "defects removed", "defects injected", "total time", "failure cost of quality", "appraisal cost of quality", "total defects"]

# TODO Graficas pendiendtes:
'''
- Size estimation error.
- Actual development time.
- Time estimation error.
- Percent compile time.
- Percent test time.
- Percent compile + test time.
- yield vs A/FR", "A/FR vs yield.
- Defect injection % by phase.
- Defect removal % by phase.
- Total cost of quality.
- Appraisal to failure ratio
'''


TIME_TOTAL_BY_PROGRAM = Coalesce(Sum(Ceil(F('program_log_time__delta_time') / 60.0)), 0)
