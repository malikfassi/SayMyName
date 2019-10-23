from peewee import CharField

from api.EncryptedConfiguration.EncryptedConfigurationExceptions import EncryptedConfigurationDoesNotExistException
from api.common.models.BaseModel import BaseModel


class EncryptedConfiguration(BaseModel):
    client_id = CharField(unique=True)
    blob = CharField()

    DoesNotExistException = EncryptedConfigurationDoesNotExistException

    @staticmethod
    def get_configuration(client_id):
        print("hey")
        data = EncryptedConfiguration.get(EncryptedConfiguration.client_id == client_id)
        print("lust")
        return data

    def serialize(self):
        return {
            'client_id': self.client_id,
            'blob': self.blob
        }
