import importlib
import sys

import bpy

# hot reload
current_package_prefix = f"{__name__}."
for name, module in sys.modules.copy().items():
    if name.startswith(current_package_prefix):
        print(f"Reloading {name}")
        importlib.reload(module)

from .auto_group_channels import AutoGroupChannelsOperator
from .clean_constant_channels import CleanConstantChannelsOperator
from .find_forgotten_fcurves import FindForgottenFcurvesOperator
from .normalize_quaternion_rotation import NormalizeQuaternionRotationOperator
from .reset_bezier_handles import ResetBezierHandlesOperator
from .select_bezier_handles import (
    SelectLeftBezierHandlesOperator,
    SelectRightBezierHandlesOperator,
)
from .toggle_viewport_focal_length import ToggleViewportFocalLengthOperator
from .save_history import save_history_register, save_history_try_unregister

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


def register_handlers(preferences, _context):
    if preferences.save_history_enabled:
        save_history_register()
    else:
        save_history_try_unregister()


def unregister_handlers():
    save_history_try_unregister()


class Preferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    save_history_enabled: bpy.props.BoolProperty(
        name="Insert Save History", default=False, update=register_handlers
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "save_history_enabled")


def register():
    bpy.utils.register_class(Preferences)

    bpy.utils.register_class(AutoGroupChannelsOperator)
    bpy.utils.register_class(CleanConstantChannelsOperator)
    bpy.utils.register_class(FindForgottenFcurvesOperator)
    bpy.utils.register_class(NormalizeQuaternionRotationOperator)
    bpy.utils.register_class(ResetBezierHandlesOperator)
    bpy.utils.register_class(SelectLeftBezierHandlesOperator)
    bpy.utils.register_class(SelectRightBezierHandlesOperator)
    bpy.utils.register_class(ToggleViewportFocalLengthOperator)

    preferences = bpy.context.preferences.addons[__name__].preferences

    register_handlers(preferences, None)


def unregister():
    bpy.utils.unregister_class(Preferences)

    bpy.utils.unregister_class(AutoGroupChannelsOperator)
    bpy.utils.unregister_class(CleanConstantChannelsOperator)
    bpy.utils.unregister_class(FindForgottenFcurvesOperator)
    bpy.utils.unregister_class(NormalizeQuaternionRotationOperator)
    bpy.utils.unregister_class(ResetBezierHandlesOperator)
    bpy.utils.unregister_class(SelectLeftBezierHandlesOperator)
    bpy.utils.unregister_class(SelectRightBezierHandlesOperator)
    bpy.utils.unregister_class(ToggleViewportFocalLengthOperator)

    unregister_handlers()


if __name__ == "__main__":
    register()
