from api.common.CommonException import CommonDoesNotExist, CommonException


class MaterialDoesNotExistException(CommonDoesNotExist):
    def __init__(self, *query, **filters):
        super().__init__('PCB', *query, **filters)
        self.code = 401


class MaterialAlreadyExistsException(CommonException):
    def __init__(self):
        super().__init__()
        self.message = "Material already exists"
        self.code = 402


class NotEnoughMaterialException(CommonException):
    def __init__(self, name, ref):
        super().__init__()
        self.message = f"Not enough material in current poste ({name}, {ref})"
        self.code = 503


class PCBNotPreparedException(CommonException):
    def __init__(self):
        super().__init__()
        self.message = f"PCB had not been prepared"
        self.code = 504
