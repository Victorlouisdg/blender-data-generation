import bpy
import numpy as np


def add_horizontal_edges(edges, rows, cols):
    for n in range(rows):
        for m in range(cols):
            if m + 1 < cols:
                i = m + n * cols
                edges.append((i, i + 1))


def add_vertical_edges(edges, rows, cols):
    for m in range(cols):
        for n in range(rows):
            if n + 1 < rows:
                i = m + n * cols
                j = m + (n + 1) * cols
                edges.append((i, j))
                

def generate_edges(rows, cols):
    edges = []
    add_horizontal_edges(edges, rows, cols)
    add_vertical_edges(edges, rows, cols)
    return edges


def create_cloth_mesh(rows, cols):
    n_masses = rows * cols
    length = 0.5
    l_rest = length / (rows - 1)

    def init_position(i, cols, l_rest):
        x = l_rest * np.floor(i / cols) - length / 2
        y = l_rest * (i % cols) - length / 2
        z = 0.0
        return np.array([x, y, z], dtype=np.float32)


    p0 = np.array([init_position(i, cols, l_rest) for i in np.arange(n_masses)])
    
    verts = p0
    edges = generate_edges(rows, cols)
    faces = [] 
    
    mesh = bpy.data.meshes.new('mesh')
    mesh.from_pydata(verts, edges, faces)
    cloth = bpy.data.objects.new("Cloth", mesh)
    bpy.context.scene.collection.objects.link(cloth)
    bpy.context.view_layer.objects.active = cloth
    
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.fill_holes()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return cloth