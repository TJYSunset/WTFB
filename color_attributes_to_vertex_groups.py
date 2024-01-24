import re

import bpy


def main(context: bpy.types.Context, lock: bool, regex: str) -> (int, int):
    obj = context.active_object
    mesh: bpy.types.Mesh = obj.data
    success = 0
    skipped = 0
    compiled_regex = re.compile(regex)
    for color_attribute in list(mesh.color_attributes):
        regex_match = compiled_regex.match(color_attribute.name)
        if regex_match is None:
            continue

        if not isinstance(color_attribute, bpy.types.FloatColorAttribute):
            skipped += 1
            continue

        vertex_group_name = regex_match.group("name")

        old_vertex_group = obj.vertex_groups.get(vertex_group_name)
        if old_vertex_group is not None:
            obj.vertex_groups.remove(vertex_group_name)
        vertex_group = obj.vertex_groups.new(name=vertex_group_name)
        vertex_group.lock_weight = lock

        for i, value in enumerate(color_attribute.data):
            vertex_group.add([i], value.color[0], "REPLACE")

        mesh.color_attributes.remove(color_attribute)

        success += 1

    return (success, skipped)


class ColorAttributesToVertexGroupsOperator(bpy.types.Operator):
    """Batch convert color attributes to vertex groups"""

    bl_idname = "mesh.wtfb_color_attributes_to_vertex_groups"
    bl_label = "Color Attributes to Vertex Groups (Might Crash!)"
    bl_options = {"REGISTER", "UNDO"}

    lock: bpy.props.BoolProperty(name="Lock", default=True)
    regex: bpy.props.StringProperty(name="Regex", default=r"^<VG>(?P<name>.+)$")

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
        (success, skipped) = main(context, self.lock, self.regex)
        if skipped == 0:
            self.report(
                {"INFO"}, f"Converted {success} color attributes to vertex groups"
            )
        else:
            self.report(
                {"WARNING"},
                f"Converted {success} color attributes to vertex groups, skipped {skipped}",
            )
        return {"FINISHED"}
