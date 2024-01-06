import bpy


def main(context, left: bool):
    for fcurve in context.selected_editable_fcurves:
        for point in fcurve.keyframe_points:
            if point.interpolation == "BEZIER":
                if left:
                    point.select_left_handle = True
                else:
                    point.select_right_handle = True


class SelectLeftBezierHandlesOperator(bpy.types.Operator):
    """Select all left handles of bezier keyframes"""

    bl_idname = "anim.wtfb_select_left_bezier_handles"
    bl_label = "Select Left Bezier Handles"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return context.selected_editable_fcurves is not None

    def execute(self, context):
        main(context, True)
        return {"FINISHED"}


class SelectRightBezierHandlesOperator(bpy.types.Operator):
    """Select all right handles of bezier keyframes"""

    bl_idname = "anim.wtfb_select_right_bezier_handles"
    bl_label = "Select Right Bezier Handles"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        try:
            return context.selected_editable_fcurves is not None
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        main(context, False)
        return {"FINISHED"}
