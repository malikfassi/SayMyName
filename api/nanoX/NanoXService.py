from peewee import IntegrityError

from api.materials.MaterialExceptions import PCBNotPreparedException
from api.materials.MaterialType import MaterialsType
from api.materials.Materials import Material
from api.nanoX.NanoX import NanoX
from api.nanoX.NanoXExceptions import PCBAlreadyScannedException


class NanoXService:
    def prepare_pcb(self, pcb_id):
        try:
            NanoX.create(pcb=pcb_id)
        except IntegrityError:
            raise PCBAlreadyScannedException()

    def _verify_previous_pcb_has_been_prepared(self, nano_x):
        if nano_x.identity:
            raise PCBNotPreparedException()

    def finalize(self):
        nano_x = NanoX.select().order_by(NanoX.id.desc()).get()
        self._verify_previous_pcb_has_been_prepared(nano_x)
        nano_x.identity = nano_x.pcb
        nano_x.display = Material.get_current_material_batch(MaterialsType.DISPLAY)
        nano_x.battery = Material.get_current_material_batch(MaterialsType.BATTERY)
        nano_x.back_cover = Material.get_current_material_batch(MaterialsType.BACK_COVER)
        nano_x.top_cover = Material.get_current_material_batch(MaterialsType.TOP_COVER)
        nano_x.button_metal = Material.get_current_material_batch(MaterialsType.BUTTON_METAL)
        nano_x.save()
        print(nano_x.serialize())
        Material.update(amount=Material.amount - 1).where(Material.id << nano_x.get_materials()).execute()

    def trace(self, nano_x_id):
        return NanoX.get(NanoX.identity == nano_x_id).serialize()
