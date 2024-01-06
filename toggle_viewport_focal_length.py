import bpy


def main(context):
    # The docs for `bpy.types.Area` claims that the first space is the active space,
    # so no need to loop through all spaces
    space = context.area.spaces[0]
    old_focal_length = space.lens
    new_focal_length = 50.0 if old_focal_length != 50.0 else 35.0
    space.lens = new_focal_length
    return (old_focal_length, new_focal_length)


class ToggleViewportFocalLengthOperator(bpy.types.Operator):
    """Toggles viewport focal length between 35mm and 50mm"""

    bl_idname = "view3d.wtfb_toggle_viewport_focal_length"
    bl_label = "Toggle Viewport Focal Length"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        try:
            return context.area.type == "VIEW_3D"
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        (old_focal_length, new_focal_length) = main(context)
        self.report(
            {"INFO"},
            f"Focal length changed from {old_focal_length}mm to {new_focal_length}mm",
        )
        return {"FINISHED"}
