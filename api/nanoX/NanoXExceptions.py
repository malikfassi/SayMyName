from api.common.CommonException import CommonDoesNotExist, CommonException


class NanoXDoesNotExistException(CommonDoesNotExist):
    def __init__(self, *query, **filters):
        super().__init__('NanoX', *query, **filters)
        self.code = 401


class PreviousPCBScannedNotAssembledException(CommonException):
    def __init__(self):
        super().__init__()
        self.code = 402
        self.message = "Previous pcb has not been assembled"


class PCBAlreadyScannedException(CommonException):
    def __init__(self):
        super().__init__()
        self.code = 403
        self.message = "PCB already scanned"
