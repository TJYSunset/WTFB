import bpy

from .auto_group_channels import AutoGroupChannelsOperator
from .clean_constant_channels import CleanConstantChannelsOperator
from .find_forgotten_fcurves import FindForgottenFcurvesOperator
from .normalize_quaternion_rotation import NormalizeQuaternionRotationOperator
from .reset_bezier_handles import ResetBezierHandlesOperator
from .select_bezier_handles import (SelectLeftBezierHandlesOperator,
                                    SelectRightBezierHandlesOperator)

bl_info = {
    "name": "WTFB",
    "author": "Todd York",
    "version": (20240105, 0),
    "blender": (4, 0, 0),
    "location": "Search Menu",
    "description": "Various personal tools for Blender",
    "warning": "Bugs are expected",
    "tracker_url": "https://github.com/tjysunset/WTFB",
    "category": "Tools",
}

def register():
    bpy.utils.register_class(AutoGroupChannelsOperator)
    bpy.utils.register_class(CleanConstantChannelsOperator)
    bpy.utils.register_class(FindForgottenFcurvesOperator)
    bpy.utils.register_class(NormalizeQuaternionRotationOperator)
    bpy.utils.register_class(ResetBezierHandlesOperator)
    bpy.utils.register_class(SelectLeftBezierHandlesOperator)
    bpy.utils.register_class(SelectRightBezierHandlesOperator)

def unregister():
    bpy.utils.unregister_class(AutoGroupChannelsOperator)
    bpy.utils.unregister_class(CleanConstantChannelsOperator)
    bpy.utils.unregister_class(FindForgottenFcurvesOperator)
    bpy.utils.unregister_class(NormalizeQuaternionRotationOperator)
    bpy.utils.unregister_class(ResetBezierHandlesOperator)
    bpy.utils.unregister_class(SelectLeftBezierHandlesOperator)
    bpy.utils.unregister_class(SelectRightBezierHandlesOperator)

if __name__ == "__main__":
    register()
