import bpy
import os
import random
from data_generation import hdri, utils, cloth_utils, transform_utils, camera_utils
import numpy as np
import mathutils


for c in range(10):
    utils.cleanup()

    directory_path = '/home/victor/Blender/Files/HDRI maps'
    #directory_path = '/home/idlab185/Blender/Files/HDRI maps'

    filename = random.choice(os.listdir(directory_path))
    filepath = os.path.join(directory_path, filename)

    hdri_rotation = 2 * np.pi * random.random()
    hdri.load(filepath, hdri_rotation)

    bpy.ops.mesh.primitive_plane_add(size=1.5)
    ground = bpy.context.active_object
    utils.select_only(ground)
    bpy.ops.object.modifier_add(type='COLLISION')
    ground.collision.cloth_friction = 50
    ground.collision.thickness_outer = 0.005

    cloth = cloth_utils.create_cloth_mesh(10, 10)

       # marking the edge crease to prevent smooth corners
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='INVERT')
    bpy.ops.mesh.select_non_manifold()
    bpy.ops.transform.edge_crease(value=1) 
    bpy.ops.object.mode_set(mode='OBJECT')

    cloth_material = bpy.data.materials.new(name="Cloth")
    cloth_material.diffuse_color = (0.8, 0.0620973, 0.0522176, 1)


    cloth_material.use_nodes = True

    cloth_bsdf = cloth_material.node_tree.nodes['Principled BSDF']
    cloth_bsdf.inputs['Base Color'].default_value = (1, 0, 0, 1)
    cloth_bsdf.inputs['Roughness'].default_value = 1
    cloth_bsdf.inputs['Sheen'].default_value = 1

    cloth.data.materials.append(cloth_material)


    utils.select_only(cloth)

    R = transform_utils.random_rotation_matrix()
    R = mathutils.Matrix(R).to_4x4()

    cloth.matrix_world = R @ cloth.matrix_world
    bpy.ops.transform.translate(value=(0, 0, 0.7))

    x = random.random() * 0.5 - 0.25
    y = random.random() * 0.5 - 0.25
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.05, location=(x, y, 0.15))

    sphere = bpy.context.active_object
    sphere_collision = sphere.modifiers.new('SphereCollision', 'COLLISION')
    sphere.collision.thickness_outer = 0.02

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
        bpy.context.scene.frame_end = 99

        for i in range(99):
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)
            if i == 70:
                utils.select_only(sphere)
                bpy.ops.object.delete() 
            
        utils.select_only(cloth)
        bpy.ops.object.modifier_apply(modifier="ClothMod")
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        
        bpy.ops.object.modifier_add(type='SUBSURF')
        
        subsurf = cloth.modifiers.new('SubsurfMod', 'SUBSURF')
        subsurf.levels = 3
        subsurf.render_levels = 3
        bpy.ops.object.shade_smooth()


    simulate(cloth)

    # Add a camera
    bpy.ops.object.camera_add(location=(0.75, 0.75, 1.1))
    camera = bpy.context.active_object
    camera.data.lens = 80 # focal length in mm
    camera_utils.look_at([0, 0, 0], camera)
       
    # Render an image
    scene = bpy.context.scene 
    scene.render.image_settings.file_format = 'PNG'
    scene.camera = camera
    scene.render.filepath = '/home/victor/Blender/datasets/cloth_100/cloth' + str(c)
    bpy.ops.render.render(write_still=True)

    print('File saved at ' + bpy.path.abspath(scene.render.filepath))