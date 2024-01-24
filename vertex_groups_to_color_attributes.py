import bpy

from .utils.try_get_weight import try_get_weight


def main(context: bpy.types.Context, locked: bool, unlocked: bool, prefix: str) -> int:
    obj = context.active_object
    mesh: bpy.types.Mesh = obj.data
    count = 0
    for group in list(obj.vertex_groups):
        if not ((locked and group.lock_weight) or (unlocked and not group.lock_weight)):
            continue

        color_name = f"{prefix}{group.name}"
        old_color_attribute = mesh.color_attributes.get(color_name)
        if old_color_attribute is not None:
            mesh.color_attributes.remove(old_color_attribute)
        color_attribute: bpy.types.FloatColorAttribute = mesh.color_attributes.new(
            color_name, "FLOAT_COLOR", "POINT"
        )

        for i in range(0, len(obj.data.vertices)):
            weight = try_get_weight(group, i)
            color_attribute.data[i].color = [weight, weight, weight, weight]

        obj.vertex_groups.remove(group)

        count += 1

    return count


class VertexGroupsToColorAttributesOperator(bpy.types.Operator):
    """Batch convert vertex groups to color attributes"""

    bl_idname = "mesh.wtfb_vertex_groups_to_color_attributes"
    bl_label = "Vertex Groups to Color Attributes (Might Crash!)"
    bl_options = {"REGISTER", "UNDO"}

    locked: bpy.props.BoolProperty(name="Locked", default=True)
    unlocked: bpy.props.BoolProperty(name="Unlocked", default=False)
    prefix: bpy.props.StringProperty(name="Prefix", default="<VG>")

    @classmethod
    def poll(cls, context):
        try:
            return (
                context.active_object is not None
                and context.active_object.type == "MESH"
            )
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        count = main(context, self.locked, self.unlocked, self.prefix)
        self.report({"INFO"}, f"Converted {count} vertex groups to color attributes")
        return {"FINISHED"}
