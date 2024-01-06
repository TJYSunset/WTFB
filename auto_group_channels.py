import bpy
import re


def main(context):
    groups = context.active_object.animation_data.action.groups

    for fcurve in context.active_object.animation_data.action.fcurves:
        if fcurve.group is not None:
            continue

        bone_name = re.search(r'bones\["(.+?)"]', fcurve.data_path).group(1)

        group = groups.get(bone_name)

        if group is not None:
            fcurve.group = group
        else:
            group = groups.new(bone_name)
            fcurve.group = group


class AutoGroupChannelsOperator(bpy.types.Operator):
    """Group ungrouped channels"""

    bl_idname = "anim.wtfb_auto_group_channels"
    bl_label = "Auto Group Channels"
    bl_options = {"REGISTER", "UNDO"}

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
