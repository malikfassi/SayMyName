from flask import Blueprint, request

from api.common.HttpRessource import HttpResource
from api.nanoX.NanoXService import NanoXService


class NanoXController:

    # material route
    nanox_routes = Blueprint('nanox', __name__)
    nanox_service = NanoXService()

    @staticmethod
    @nanox_routes.route('/nanox/prepare/<pcb_id>', methods=['POST'])
    def prepare_pcb(pcb_id):
        NanoXController.nanox_service.prepare_pcb(pcb_id)
        return HttpResource.success()

    @staticmethod
    @nanox_routes.route('/nanox/finalize', methods=['POST'])
    def finalize():
        NanoXController.nanox_service.finalize()
        return HttpResource.success()

    @staticmethod
    @nanox_routes.route('/nanox/<nano_x_id>', methods=['GET'])
    def trace_nano_x(nano_x_id):
        nano_x = NanoXController.nanox_service.trace(nano_x_id)
        return HttpResource.success(nano_x)
