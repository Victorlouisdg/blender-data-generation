from data_generation import hdri
import os
import random

directory_path = '/home/victor/Blender/Files/HDRI maps'
filename = random.choice(os.listdir(directory_path))
filepath = os.path.join(directory_path, filename)

hdri.load(filepath)

