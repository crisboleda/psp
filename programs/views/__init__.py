
from .programs import (AdminListProgramView, CreateProgramView, ProgrammerListProgramView, 
                        DetailProgramView)

from .parts_of_code import (CreatePartProgramView, UpdateBaseProgramView, UpdateReusedPartView,
                            UpdateNewPartView, DeleteReusedPartView, DeleteNewPartView,
                            DeleteBasePartView)

from .pip import (ListPIPView,)

from .report import (ReportView, ReportRetrieveUpdateDestroyView, UpdateReportView)