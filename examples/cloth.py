import bpy
import os
import random
from data_generation import hdri, utils, cloth_utils, transform_utils
import numpy as np
import mathutils

utils.cleanup()

directory_path = '/home/victor/Blender/Files/HDRI maps'
directory_path = '/home/idlab185/Blender/Files/HDRI maps'

filename = random.choice(os.listdir(directory_path))
filepath = os.path.join(directory_path, filename)

hdri.load(filepath)

bpy.ops.mesh.primitive_plane_add(size=1.5)
ground = bpy.context.active_object
utils.select_only(ground)
bpy.ops.object.modifier_add(type='COLLISION')
ground.collision.cloth_friction = 50
ground.collision.thickness_outer = 0.001

cloth = cloth_utils.create_cloth_mesh(10, 10)

   # marking the edge crease to prevent smooth corners
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='INVERT')
bpy.ops.mesh.select_non_manifold()
bpy.ops.transform.edge_crease(value=1) 
bpy.ops.object.mode_set(mode='OBJECT')

cloth_material = bpy.data.materials.new(name="Cloth")
cloth_material.use_nodes = True
cloth_material.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value = (1, 0, 0, 1)

cloth.data.materials.append(cloth_material)

utils.select_only(cloth)

R = transform_utils.random_rotation_matrix()
R = mathutils.Matrix(R).to_4x4()

cloth.matrix_world = R @ cloth.matrix_world
bpy.ops.transform.translate(value=(0, 0, 0.5))


def simulate(cloth):
    cloth_mod = cloth.modifiers.new("ClothMod", 'CLOTH')
    
    ## Cloth Settings
    cloth_mod.collision_settings.use_self_collision = True
    cloth_mod.collision_settings.distance_min = 0.001
    cloth_mod.collision_settings.self_distance_min = 0.003
    cloth_mod.collision_settings.self_friction = 50
    
    cloth_mod.settings.tension_stiffness = 5
    cloth_mod.settings.compression_stiffness = 5
    cloth_mod.settings.shear_stiffness = 1
    cloth_mod.settings.bending_stiffness = 0.1
    
    cloth_mod.settings.tension_damping = 100
    cloth_mod.settings.compression_damping = 100
    cloth_mod.settings.shear_damping = 5
    cloth_mod.settings.bending_damping = 0.5

    bpy.context.scene.frame_set(0) 
    for i in range(99):
        bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
        
    bpy.ops.object.modifier_apply(modifier="ClothMod")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    bpy.ops.object.modifier_add(type='SUBSURF')
    
    subsurf = cloth.modifiers.new('SubsurfMod', 'SUBSURF')
    subsurf.levels = 3
    subsurf.render_levels = 3
    bpy.ops.object.shade_smooth()


simulate(cloth)