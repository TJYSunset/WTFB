import bpy

from .utils.multiline_msgbox import multiline_msgbox


def main(context):
    list = []
    for fcurve in context.active_object.animation_data.action.fcurves:
        points = fcurve.keyframe_points
        if not points or len(points) <= 1:
            continue

        all_constant_or_linear = True
        for frame in points:
            if frame.interpolation != "CONSTANT" and frame.interpolation != "LINEAR":
                all_constant_or_linear = False

        if not all_constant_or_linear:
            continue

        list.append(fcurve.data_path)
        multiline_msgbox("Find Forgotten F-Curves", list)


class FindForgottenFcurvesOperator(bpy.types.Operator):
    """Tooltip"""

    bl_idname = "anim.wtfb_find_forgotten_fcurves"
    bl_label = "Find Forgotten F-Curves"

    @classmethod
    def poll(cls, context):
        try:
            return bpy.context.active_object.animation_data.action.fcurves is not None
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        main(context)
        return {"FINISHED"}
