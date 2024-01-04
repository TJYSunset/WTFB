import bpy

def main(context):
    for bone in context.selected_pose_bones:
        bone.rotation_quaternion = bone.rotation_quaternion.normalized()

class NormalizeQuaternionRotationOperator(bpy.types.Operator):
    """Normalize quaternion rotation for selected bones"""
    bl_idname = "pose.wtfb_normalize_quaternion_rotation"
    bl_label = "Normalize Quaternion Rotation"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return context.selected_pose_bones is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}
