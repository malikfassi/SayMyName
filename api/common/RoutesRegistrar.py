from api.common.StatusController import StatusController
from api.materials.MaterialsController import MaterialsController
from api.nanoX.NanoXController import NanoXController


class RoutesRegistrar:

    BLUEPRINTS = [
        StatusController.status_routes,
        MaterialsController.material_routes,
        NanoXController.nanox_routes
    ]

    def __init__(self, app):
        self.app = app

    def register(self):
        for blueprint in self.BLUEPRINTS:
            self.app.register_blueprint(blueprint)
