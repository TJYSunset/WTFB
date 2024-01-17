import bpy


def try_get_weight(group: bpy.types.VertexGroup, index: int):
    try:
        return group.weight(index)
    except:
        return 0.0


def main(
    context: bpy.types.Context, source_name: str, target_name: str, keep_source: bool
) -> (bool, str):
    obj = context.active_object
    source = obj.vertex_groups.get(source_name)
    target = obj.vertex_groups.get(target_name)
    if source is None:
        return (False, f"Vertex group {source_name} not found")
    if target is None:
        return (False, f"Vertex group {target_name} not found")

    original_mode = context.object.mode
    bpy.ops.object.mode_set(mode="OBJECT")
    
    for i in range(0, len(context.active_object.data.vertices)):
        source_weight = try_get_weight(source, i)
        if source_weight > 0:
            target.add([i], source_weight, "ADD")
        if not keep_source:
            source.remove([i])
            
    bpy.ops.object.mode_set(mode=original_mode)

    return (True, f"Successfully moved {source_name} to {target_name}")


class MoveVertexWeightsOperator(bpy.types.Operator):
    """Adds weights from one vertex group to another"""

    bl_idname = "mesh.wtfb_move_vertex_weights"
    bl_label = "Move Vertex Weights"
    bl_options = {"REGISTER", "UNDO"}

    source_name: bpy.props.StringProperty(name="Source Vertex Group")
    target_name: bpy.props.StringProperty(name="Target Vertex Group")
    keep_source: bpy.props.BoolProperty(name="Keep Source", default=False)

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
        (success, message) = main(
            context, self.source_name, self.target_name, self.keep_source
        )
        self.report({"INFO" if success else "ERROR"}, message)
        return {"FINISHED"}
