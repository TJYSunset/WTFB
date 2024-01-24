import itertools

import bmesh
import bpy

from .utils.try_get_weight import try_get_weight


def main(context: bpy.types.Context):
    mesh = bmesh.from_edit_mesh(context.active_object.data)
    islands = list[list[int]]()
    if "EDGE" not in mesh.select_mode:
        islands.append(list(x.index for x in mesh.verts if x.select))
    else:
        loops = list[list[bmesh.types.BMEdge]]()
        remaining_edges: list[bmesh.types.BMEdge] = list(
            x for x in mesh.edges if x.select
        )
        if not remaining_edges:
            return

        while remaining_edges:
            loop = list[bmesh.types.BMEdge]()

            def search(edge: bmesh.types.BMEdge):
                loop.append(edge)
                remaining_edges.remove(edge)
                for neighbor in itertools.chain(
                    edge.verts[0].link_edges, edge.verts[1].link_edges
                ):
                    if neighbor in remaining_edges:
                        search(neighbor)

            search(remaining_edges[0])
            loops.append(loop)

        for loop in loops:
            island = set[int]()
            for edge in loop:
                island.add(edge.verts[0].index)
                island.add(edge.verts[1].index)
            islands.append(list(island))

    if not islands:
        return

    bpy.ops.object.mode_set(mode="OBJECT")

    for indices in islands:
        for group in context.active_object.vertex_groups:
            if group.lock_weight:
                continue

            average = sum(try_get_weight(group, x) for x in indices) / len(indices)

            if average > 0:
                group.add(indices, average, "REPLACE")

    bpy.ops.object.mode_set(mode="EDIT")

    mesh.free()


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
