import bpy
import os
import random
import math
from data_generation import hdri, utils, camera_utils
from urdf_importer import import_urdf

utils.cleanup()

# Load random HDRI maps from directory
directory_path = '/home/victor/Blender/Files/HDRI maps'
filename = random.choice(os.listdir(directory_path))
filepath = os.path.join(directory_path, filename)
hdri.load(filepath)

# Load robot via URDF file
import_urdf.import_urdf('/home/victor/ur10.urdf')
armature = bpy.context.active_object

# Change the robot pose
bpy.ops.object.mode_set(mode='POSE')
armature.pose.bones['shoulder_lift_joint'].rotation_euler[1] = - math.pi / 4
armature.pose.bones['elbow_joint'].rotation_euler[1] = math.pi / 2
bpy.ops.object.mode_set(mode='OBJECT')

# Add a camera
bpy.ops.object.camera_add(location=(2, 2, 1))
camera = bpy.context.active_object
camera_utils.look_at([0, 0, 0], camera)
   
# Render an image
scene = bpy.context.scene 
scene.render.image_settings.file_format = 'PNG'
scene.camera = camera
scene.render.filepath = 'ur10'
bpy.ops.render.render(write_still=True)

print('File saved at ' + bpy.path.abspath(scene.render.filepath))