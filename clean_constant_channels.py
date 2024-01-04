import bpy

def main(context, threshold, hide, keep_time):
    for fcurve in context.active_object.animation_data.action.fcurves:
        points = fcurve.keyframe_points
        if not points:
            if hide:
                fcurve.hide = True
            continue
        
        points.sort()
        first_time = points[0].co.x
        first_value = points[0].co.y
        
        noop = False
        for frame in points[1:]:
            if abs(frame.co.y - first_value) > threshold:
                noop = True
        if noop:
            continue
        
        points.clear()
        new_frame = points.insert(first_time if keep_time else 0, first_value)
        new_frame.interpolation = "CONSTANT"
        
        if hide:
            fcurve.hide = True

class CleanConstantChannelsOperator(bpy.types.Operator):
    """Delete all but the first keyframe for constant F-Curves in the active action"""
    bl_idname = "anim.wtfb_clean_constant_channels"
    bl_label = "Clean Constant Channels"
    bl_options = {'REGISTER', 'UNDO'}
    
    threshold: bpy.props.FloatProperty(name="Threshold", default=0.00001, min=0, soft_max=0.1, precision=6)
    hide: bpy.props.BoolProperty(name="Hide Constant Channels", default=True)
    keep_time: bpy.props.BoolProperty(name="Keep Start Time", default=False)

    @classmethod
    def poll(cls, context):
        return bpy.context.active_object.animation_data.action.fcurves is not None

    def execute(self, context):
        main(context, self.threshold, self.hide, self.keep_time)
        return {'FINISHED'}
