from api.common.CommonException import CommonDoesNotExist


class EncryptedConfigurationDoesNotExistException(CommonDoesNotExist):
    def __init__(self, *query, **filters):
        super().__init__('EncryptedConfiguration', *query, **filters)
        self.code = 901