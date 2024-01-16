import bpy


def main(context):
    # The docs for `bpy.types.Area` claims that the first space is the active space,
    # so no need to loop through all spaces
    space: bpy.types.SpaceView3D = context.area.spaces[0]
    shading = space.shading
    if shading.light == "MATCAP":
        shading.light = "FLAT"
        shading.show_shadows = True
        shading.show_cavity = True
    else:
        shading.light = "MATCAP"
        shading.show_shadows = False
        shading.show_cavity = False


class ToggleViewportShadingOperator(bpy.types.Operator):
    """Toggles viewport shading between MatCap and flat + shadows + curvature"""

    bl_idname = "view3d.wtfb_toggle_viewport_shading"
    bl_label = "Toggle Viewport Shading"
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        try:
            return context.area.type == "VIEW_3D"
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        main(context)
        return {"FINISHED"}
