import bpy
import random
import math
from . import node_utils

def load(filepath, z_rotation=0.0):
    world_tree = bpy.data.worlds['World'].node_tree

    for node in world_tree.nodes:
        world_tree.nodes.remove(node)
        
    world_output_node = world_tree.nodes.new("ShaderNodeOutputWorld")

    environment_texture_node = world_tree.nodes.new("ShaderNodeTexEnvironment")
    node_utils.place(environment_texture_node, world_output_node, 'left')

    world_tree.links.new(
        environment_texture_node.outputs["Color"], 
        world_output_node.inputs["Surface"]
    )

    environment_texture_node.image = bpy.data.images.load(filepath)

    mapping_node = world_tree.nodes.new("ShaderNodeMapping")
    node_utils.place(mapping_node,  environment_texture_node, 'left')
    world_tree.links.new(
        mapping_node.outputs["Vector"], 
        environment_texture_node.inputs["Vector"]
    )

    texture_coordinate_node = world_tree.nodes.new("ShaderNodeTexCoord")
    node_utils.place(texture_coordinate_node, mapping_node, 'left')
    world_tree.links.new(
        texture_coordinate_node.outputs["Generated"], 
        mapping_node.inputs["Vector"]
    )

    mapping_node.inputs["Rotation"].default_value[2] = random.random() * 2 * math.pi