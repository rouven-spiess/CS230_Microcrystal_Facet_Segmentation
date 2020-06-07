# CS230-Microcrystal-Facet-Segmentation
Microcrystal facet segmentation algorithm based on U-NET architecture.

## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

## General info
The goal of this project is to build an appropriate CNN architecture that is able to perform semantic segmentation of cuprous oxide Cu2O nanocrystal facets. 

## Baseline Model
keras implementation (https://github.com/divamgupta/image-segmentation-keras/)
## Screenshots
![Example screenshot](image.png)

## Technologies
* python - version 3.6.5
* keras - version 2.3.0
* keras_segmentation 
* opencv_python - version 4.2.0.32
* Augmentor - version 0.2.8

## Setup
Available soon
<!--Describe how to install / setup your local environement / add link to demo version.-->

## Code Examples
Show examples of usage:
```
from keras_segmentation.models.unet import unet_mini

model = unet_mini(n_classes=4,  input_height=96, input_width=96  )

model.train(
    train_images = "Dataset/train/",
    train_annotations = "Dataset/train_labels/",
    checkpoints_path = "Dataset/checkpoints",
    val_images = "Dataset/test/",
    val_annotations = "Dataset/test_labels/",
    epochs=50, validate=True, batch_size=8, 
    optimizer_name="adam",
    gen_use_multiprocessing=True,
    auto_resume_checkpoint=False,
    val_batch_size=2,
)
```

## Features
List of features ready and TODOs for future development
* Train 3 different U-NET variants

To-do list:
* Wrap code and make setup.py

## Status
Project is: _in progress_ <!-- a normal html comment _finished_, _no longer continue_ and why?-->

<!--## Inspiration-->
<!--Add here credits. Project inspired by..., based on...-->

<!--## Contact-->
<!--Created by [@flynerdpl](https://www.flynerd.pl/) - feel free to contact me!-->
