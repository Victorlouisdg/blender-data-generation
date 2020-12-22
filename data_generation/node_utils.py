from mathutils import Vector

def place(node, reference_node, direction, margin=50):
    if direction in ['left', 'right']:
        displacement = Vector([node.width + margin, 0])
    if direction in ['above', 'below']:
        displacement = Vector([0, node.height + margin])
    if direction in ['left', 'below']:
        displacement *= -1
    node.location = reference_node.location + displacement