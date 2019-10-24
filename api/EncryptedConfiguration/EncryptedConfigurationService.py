from peewee import DoesNotExist

from api.EncryptedConfiguration.EncryptedConfiguration import EncryptedConfiguration
from api.common.CommonException import BadFormatException
from api.common.singleton import singleton


@singleton
class EncryptedConfigurationService:

    def get(self, client_id):
        return EncryptedConfiguration.get_configuration(client_id).serialize()

    def save(self, data):
        client_id, blob = self._extract_data(data)
        try:
            encrypted_configuration = EncryptedConfiguration.get(client_id)
            encrypted_configuration.blob = blob
            encrypted_configuration.save()
        except DoesNotExist:
            EncryptedConfiguration.create(client_id=client_id, blob=blob)

    def _extract_data(self, data):
        try:
            return data['client_id'], data['blob']
        except KeyError:
            raise BadFormatException
