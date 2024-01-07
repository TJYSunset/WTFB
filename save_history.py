import bpy
from bpy.app.handlers import persistent


@persistent
def wtfb_save_history_handler(_scene):
    bpy.ops.ed.undo_push(message="<💾>")


def save_history_register():
    bpy.app.handlers.save_pre.append(wtfb_save_history_handler)


def save_history_try_unregister():
    try:
        bpy.app.handlers.save_pre.remove(wtfb_save_history_handler)
    except:
        pass
