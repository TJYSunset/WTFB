import bmesh
import bpy


def try_get_weight(group: bpy.types.VertexGroup, index: int):
    try:
        return group.weight(index)
    except:
        return 0.0


def main(context: bpy.types.Context):
    mesh = bmesh.from_edit_mesh(context.active_object.data)
    indices = [x.index for x in mesh.verts if x.select]
    if not indices:
        return

    for group in context.active_object.vertex_groups:
        if group.lock_weight:
            continue

        average = sum(try_get_weight(group, x) for x in indices) / len(indices)

        bpy.ops.object.editmode_toggle()
        if average > 0:
            group.add(indices, average, "REPLACE")
        bpy.ops.object.editmode_toggle()


class AverageVertexWeightsOperator(bpy.types.Operator):
    """Averages unlocked vertex weights for selected vertices in the active object"""

    bl_idname = "mesh.wtfb_average_vertex_weights"
    bl_label = "Average Vertex Weights"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        try:
            return context.mode == "EDIT_MESH"
        except Exception as ex:
            print(f"{cls}: poll() error: {repr(ex)}")
            return False

    def execute(self, context):
        main(context)
        return {"FINISHED"}
