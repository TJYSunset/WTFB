import bpy


def try_get_weight(group: bpy.types.VertexGroup, index: int):
    try:
        return group.weight(index)
    except:
        return 0.0
