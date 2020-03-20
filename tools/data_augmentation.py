import Augmentor
path = "/Path/to/dataset/"
subfolder = "train" #e.g. "train"

p = Augmentor.Pipeline(path + subfolder)

# Augmentation parameters
p.crop_by_size(1, 96, 96, centre=False)
p.flip_left_right(0.75)
p.flip_top_bottom(0.75)
p.rotate_random_90(1)
p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
p.shear(0.5, 3, 3)
p.random_brightness(0.5, 0.8, 1.2)
p.random_contrast(1.0, 0.5, 3.0)
p.zoom(1, min_factor=1.0, max_factor=1.6)
p.random_distortion(0.5, 5, 5, 1)
p.resize(probability=1.0, width=96, height=96)    

p.ground_truth(path + subfolder + "_labels")

parameters ="""
p.crop_by_size(1, 96, 96, centre=False)
p.flip_left_right(0.75)
p.flip_top_bottom(0.75)
p.rotate_random_90(1)
p.rotate(probability=0.7, max_left_rotation=10, max_right_rotation=10)
p.shear(0.5, 3, 3)
p.random_brightness(0.5, 0.8, 1.2)
p.random_contrast(1.0, 0.5, 3.0)
p.zoom(1, min_factor=1.0, max_factor=1.6)
p.random_distortion(0.5, 5, 5, 1)
p.resize(probability=1.0, width=96, height=96)  
"""

with open(path + "augmentation_" + subfolder + ".txt", "w") as text_file:
    text_file.write(parameters)
    
p.sample(250)
