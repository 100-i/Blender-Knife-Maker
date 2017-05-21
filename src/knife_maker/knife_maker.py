bl_info = {
    "name": "KnifeMaker",
    "author": "100i",
    "version": (0, 1),
    "blender": (2, 78),
    "location": "View3D > Add > Mesh",
}

import bpy
from mathutils import *
from math import *
from bpy.props import *


# Function to construct the knife.
def make_knife():
    # Use a rectangular prism as a starting place for shaping the blade.
    def make_blank():
        bpy.ops.mesh.primitive_cube_add()
        ob = bpy.context.object
        ob.scale = (1, .15, .075)

    # Create the edge profile of a blade using a nurbs curve.
    def nurb_blade():
        bpy.ops.curve.primitive_nurbs_curve_add()

        ob = bpy.context.active_object

        bpy.ops.object.modifier_add(type='MIRROR')

        ob.modifiers["Mirror"].use_x = False
        ob.modifiers["Mirror"].use_y = True

    # TODO - Add UI panel to select construction method
    # Call the appropriate function.
    make_blank()

# Class object used by Blender to add the mesh primitive to the backed and UI.
class KnifeMaker(bpy.types.Operator):
    bl_idname = "mesh.primitive_knife_add"
    bl_label = "Make a Knife"
    bl_description = "Make a knife."
    bl_options = { 'REGISTER', 'UNDO' }

    def execute(self, context):
        make_knife()
        return { 'FINISHED' }

    def invoke(self, context, event):
        self.execute(context)
        return { 'FINISHED' }

def menu_func(self, context):
    self.layout.operator(KnifeMaker.bl_idname, text='KnifeMaker', icon='PLUGIN')

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_remove.append(menu_func)

if __name__ == '__main__':
    register()
