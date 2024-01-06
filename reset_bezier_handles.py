import bpy
import mathutils

def main(context):
    for fcurve in context.selected_editable_fcurves:
        for point in fcurve.keyframe_points:
            if point.interpolation == "BEZIER":
                point.handle_left_type = "ALIGNED"
                point.handle_right_type = "ALIGNED"
                point.handle_left = point.co + mathutils.Vector((-1, 0))
                point.handle_right = point.co + mathutils.Vector((1, 0))

class ResetBezierHandlesOperator(bpy.types.Operator):
    """Sanitizes all editable F-Curves' bezier handles"""
    bl_idname = "anim.wtfb_reset_bezier_handles"
    bl_label = "Reset Bezier Handles"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        try:
            return context.selected_editable_fcurves is not None
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        main(context)
        return {'FINISHED'}
