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
    ## Translate on local axis.
    # The inverse of the world matrix is used to align the translation
    # vector to the local.
    def translate(ob, _vec):
        # Pick a translation vector.
        vec = Vector(_vec)

        # Get an inverted copy the world matrix.
        inv = ob.matrix_world.copy()
        inv.invert()

        # Set the object's location.
        ob.location += vec * inv

    ## Use a rectangular prism as a starting place for shaping the blade.
    def make_blank():
        bpy.ops.mesh.primitive_cube_add()
        ob = bpy.context.object
        ob.scale = (1, .15, .075)
        return ob

    ## Handles can be made from one, two or more pieces of a material.
    def make_handle():
        # Create handle blank.
        bpy.ops.mesh.primitive_cube_add()
        ob = bpy.context.object
        ob.scale = (1, .15, .075)

        # Translate object
        translate(ob, (0.0, 0.0, 0.5))

        # Set the object's group.
        bpy.ops.object.group_add()
        bpy.data.groups["Group"].name = "Handle"

        # Set layer
        bpy.ops.scene.namedlayer_move_to_layer(layer_idx=1)

        # Shape handle
        # Duplicate and flip
        return ob

    ## Create the edge profile of a blade using a nurbs curve.
    def nurb_blade():
        bpy.ops.curve.primitive_nurbs_curve_add()

        ob = bpy.context.active_object

        bpy.ops.object.modifier_add(type='MIRROR')

        ob.modifiers["Mirror"].use_x = False
        ob.modifiers["Mirror"].use_y = True
        ob.modifiers["Mirror"].use_z = False

    def process_blank(ob):
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.mesh.subdivide(number_cuts=1)
        #bpy.context.tool_settings.mesh_select_mode = [False, False, True]
        #bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        #ob.mesh.vertice[1].select = True

    # TODO - Add UI panel to select construction method
    # Call the appropriate function.
    make_handle()
    process_blank( make_blank() )

## Class object used by Blender to add the mesh primitive to the backed and UI.
class KnifeMaker(bpy.types.Operator):
    bl_idname = "mesh.primitive_knife_add"
    bl_label = "Make a Knife"
    bl_description = "Make a knife."
    bl_options = { 'REGISTER', 'UNDO' }

    edit = BoolProperty(name='',
                        decription='',
                        default=False,
                        options={'HIDDEN'})


    ## Property for length of knife blank.
    length = FloatProperty(name="Blank Length",
                           description="Length of the knife blank",
                           min=0.1,
                           max=1.0,
                           default=1.0)

    ## Set length of the blade, proportional to the knife blank.
    blade_length = FloatProperty(name="Blade Length",
                                 description="Length of the blade by ratio",
                                 min=0.1,
                                 max=1.0,
                                 default=.5)

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
