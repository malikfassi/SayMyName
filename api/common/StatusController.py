from flask import Blueprint
from api.common.HttpRessource import HttpResource


class StatusController:

    status_routes = Blueprint('status', __name__)

    @staticmethod
    @status_routes.route('/_health', methods=['GET'])
    def get_health():
        return HttpResource.success()

    @staticmethod
    @status_routes.route('/_version', methods=['GET'])
    def get_status():
        version_file = open('VERSION', 'r')
        status = {'version': version_file.readline().strip()}
        return HttpResource.success(status)

