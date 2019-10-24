from peewee import CharField, IntegerField

from api.common.models.BaseModel import BaseModel
from api.common.models.DateTimeTZField import DateTimeTzField
from api.materials.MaterialExceptions import MaterialDoesNotExistException, NotEnoughMaterialException
from api.materials.MaterialType import MaterialsType


class Material(BaseModel):
    batch_number = CharField()
    reference = CharField()
    amount = IntegerField()
    production_date = DateTimeTzField()
    lost = IntegerField(default=0)

    DoesNotExistException = MaterialDoesNotExistException

    class Meta:
        indexes = (
            # create a unique on batch_number and reference
            (('batch_number', 'reference'), True),
        )

    @staticmethod
    def get_current_material_batch(material_type):
        try:
            return Material.get((Material.reference == material_type.value) & (Material.amount > 0))
        except MaterialDoesNotExistException:
            raise NotEnoughMaterialException(material_type.name, material_type.value)

    def get_batch_ref(self):
        return {
            'reference': self.reference,
            'type': self.get_part_type(self.reference),
            'batch_number': self.batch_number,
            'production_date': self.production_date
        }

    def get_part_type(self, ref):
        try:
            return MaterialsType(ref).name
        except:
            return None

    def serialize(self):
        return {
            'id': self.id,
            'reference': self.reference,
            'amount': self.amount,
            'production_date': self.production_date,
            'batch_number': self.batch_number,
            'lost': self.lost,
            'type': self.get_part_type(self.reference)
        }
