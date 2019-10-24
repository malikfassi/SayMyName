from flask import Blueprint, request

from api.EncryptedConfiguration.EncryptedConfigurationService import EncryptedConfigurationService
from api.common.HttpRessource import HttpResource


class EncryptedConfigurationController:

    # encrypted configuration route
    encrypted_configuration_routes = Blueprint('encrypted_configuration', __name__)
    encrypted_configuration_service = EncryptedConfigurationService()

    @staticmethod
    @encrypted_configuration_routes.route('/<client_id>', methods=['GET'])
    def get_configuration(client_id):
        response = EncryptedConfigurationController.encrypted_configuration_service.get(client_id)
        return HttpResource.success(response)

    @staticmethod
    @encrypted_configuration_routes.route('/', methods=['POST'])
    def create_configuration():
        EncryptedConfigurationController.encrypted_configuration_service.save(request.form.to_dict())
        return HttpResource.success()
