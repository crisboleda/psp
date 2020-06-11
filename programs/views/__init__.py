
from .programs import (AdminListProgramView, CreateProgramView, ProgrammerListProgramView, 
                        DetailProgramView)

from .parts_of_code import (CreatePartProgramView, UpdateBaseProgramView, UpdateReusedPartView,
                            UpdateNewPartView, DeleteReusedPartView, DeleteNewPartView,
                            DeleteBasePartView)

from .pip import (ListPIPView, UpdatePIPView, RetrieveDestroyPIPView)

from .report import (ReportView, ReportRetrieveDestroyView, UpdateReportView)


from .summary import (DataDefectInjectedView, DataTimePerPhaseView, DataDefectsRemovedView)