import bpy


def main(assign_material, assign_object, reset):
    if assign_material:
        if reset:
            for material in bpy.data.materials:
                if material.library is None:
                    material.pass_index = 0
        else:
            used_indices = set[int]()
            for material in bpy.data.materials:
                if material.pass_index != 0:
                    used_indices.add(material.pass_index)

            i = 1
            for material in bpy.data.materials:
                while i in used_indices:
                    i += 1
                if material.library is None and material.pass_index == 0:
                    material.pass_index = i
                    i += 1

    if assign_object:
        if reset:
            for obj in bpy.data.objects:
                if obj.library is None:
                    obj.pass_index = 0
        else:
            used_indices = set[int]()
            for obj in bpy.data.objects:
                if obj.pass_index != 0:
                    used_indices.add(obj.pass_index)

            i = 1
            for obj in bpy.data.objects:
                while i in used_indices:
                    i += 1
                if obj.library is None and obj.pass_index == 0:
                    obj.pass_index = i
                    i += 1


class AutoPassIndexOperator(bpy.types.Operator):
    """Assigns an unique pass index to every zero-indexed local material and object in file"""

    bl_idname = "mesh.wtfb_auto_pass_index"
    bl_label = "Auto Pass Index"
    bl_options = {"REGISTER", "UNDO"}

    assign_material: bpy.props.BoolProperty(name="Material", default=True)
    assign_object: bpy.props.BoolProperty(name="Object", default=True)
    reset: bpy.props.BoolProperty(name="Reset To Zero", default=False)

    @classmethod
    def poll(cls, context):
        try:
            return True
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        main(self.assign_material, self.assign_object, self.reset)
        return {"FINISHED"}
