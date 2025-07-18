import bpy
import os
from bpy.types import Panel, Operator
from bpy.props import StringProperty
from bpy_extras.io_utils import ExportHelper


# Operator to save the screenshot
class VIEW3D_OT_screenshot_save(Operator, ExportHelper):
    bl_idname = "view3d.screenshot_save"
    bl_label = "Save Screenshot"
    bl_description = "Take a screenshot of the 3D Viewport and save it"
    bl_options = {'REGISTER'}

    filename_ext = ".png"
    filter_glob: StringProperty(default="*.png", options={'HIDDEN'})

    def execute(self, context):
        # Get the current area and region
        for area in context.window.screen.areas:
            if area.type == 'VIEW_3D':
                for region in area.regions:
                    if region.type == 'WINDOW':
                        override = {
                            'window': context.window,
                            'screen': context.screen,
                            'area': area,
                            'region': region
                        }

                        # Save the screenshot
                        bpy.ops.screen.screenshot(override, filepath=self.filepath, full=True)
                        self.report({'INFO'}, f"Screenshot saved to: {self.filepath}")
                        return {'FINISHED'}

        self.report({'WARNING'}, "3D Viewport not found")
        return {'CANCELLED'}


# UI Panel in N-Panel
class VIEW3D_PT_screenshot_panel(Panel):
    bl_label = "Screenshot Tool"
    bl_idname = "VIEW3D_PT_screenshot_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Screenshot Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("view3d.screenshot_save", icon='FILE_IMAGE')


# Register Classes
classes = (
    VIEW3D_OT_screenshot_save,
    VIEW3D_PT_screenshot_panel,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
