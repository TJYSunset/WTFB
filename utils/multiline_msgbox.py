import bpy

def multiline_msgbox(title, messages, icon='INFO'):
    def draw(self, context):
        for message in messages:
            self.layout.label(text=message)
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)
