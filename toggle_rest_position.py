import bpy


def main(context: bpy.types.Context):
    for obj in context.selectable_objects:
        if obj.type == "ARMATURE":
            armature: bpy.types.Armature = obj.data
            armature.pose_position = (
                "POSE" if armature.pose_position != "POSE" else "REST"
            )


class ToggleRestPositionOperator(bpy.types.Operator):
    """Toggles rest position for all armatures in scene"""

    bl_idname = "armature.wtfb_toggle_rest_position"
    bl_label = "Toggle Rest Position"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        try:
            return True
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        main(context)
        return {"FINISHED"}
