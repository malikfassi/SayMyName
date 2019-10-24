from datetime import datetime, timezone

from peewee import IntegrityError

from api.common.CommonException import BadFormatException
from api.materials.MaterialExceptions import MaterialAlreadyExistsException
from api.materials.Materials import Material


class MaterialsService:

    def create(self, data):
        data = self._extract_data(data)
        try:
            Material.create(**data)
        except IntegrityError as e:
            raise MaterialAlreadyExistsException()

    def get_active_batches(self):
        materials = Material.select().where(Material.amount > 0)
        return [material.serialize() for material in materials]

    def get_all_batches(self):
        materials = Material.select()
        return [material.serialize() for material in materials]

    def prune_current_batch(self, batch_id):
        Material.update(amount=0, lost=Material.amount).where(Material.id == batch_id).execute()

    def _extract_data(self, data):
        try:
            production_date = data['production_date']
            return {'production_date': datetime.strptime(production_date, '%Y%m').replace(tzinfo=timezone.utc),
                    'amount': data['amount'],
                    'reference': data['reference'],
                    'batch_number': data['batch_number']}
        except KeyError:
            raise BadFormatException
