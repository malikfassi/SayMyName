from flask import Blueprint, request

from api.common.HttpRessource import HttpResource
from api.materials.MaterialsService import MaterialsService


class MaterialsController:

    # material route
    material_routes = Blueprint('encrypted_configuration', __name__)
    material_service = MaterialsService()

    @staticmethod
    @material_routes.route('/materials', methods=['POST'])
    def create_material():
        MaterialsController.material_service.create(request.form)
        return HttpResource.success()

    @staticmethod
    @material_routes.route('/materials/current', methods=['GET'])
    def get_current_materials():
        response = MaterialsController.material_service.get_active_batches()
        return HttpResource.success(response)

    @staticmethod
    @material_routes.route('/materials/all', methods=['GET'])
    def get_all_materials():
        response = MaterialsController.material_service.get_all_batches()
        return HttpResource.success(response)

    @staticmethod
    @material_routes.route('/materials/<material_id>', methods=['POST'])
    def prune_batch(material_id):
        MaterialsController.material_service.prune_current_batch(material_id)
        return HttpResource.success()
