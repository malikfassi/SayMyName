from api.EncryptedConfiguration.EncryptedConfigurationController import EncryptedConfigurationController
from api.common.StatusController import StatusController


class RoutesRegistrar:

    BLUEPRINTS = [
        StatusController.status_routes,
        EncryptedConfigurationController.encrypted_configuration_routes
    ]

    def __init__(self, app):
        self.app = app

    def register(self):
        for blueprint in self.BLUEPRINTS:
            self.app.register_blueprint(blueprint)