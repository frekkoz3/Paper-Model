r"""
     _____                        __  __           _      _ 
    |  __ \                      |  \/  |         | |    | |
    | |__) |_ _ _ __   ___ _ __  | \  / | ___   __| | ___| |
    |  ___/ _` | '_ \ / _ \ '__| | |\/| |/ _ \ / _` |/ _ \ |
    | |  | (_| | |_) |  __/ |    | |  | | (_) | (_| |  __/ |
    |_|   \__,_| .__/ \___|_|    |_|  |_|\___/ \__,_|\___|_|
                | |                                          
                |_|                         

    A simple rule-based model to generate realistical newspapers' pages for the training of the YOLO-Layout model.
"""
from ultralytics import YOLO
from src.fine_tuning.data_gen import generate_train_and_validation_set

from pathlib import Path

if __name__ == '__main__':

    # This is a simple fine tuning routine for a doclayout-yolo model
    # This is not complete. Augmentation should be included. 
    # Also parallelization of the generation process.
    # And deletion of the artifacts once the training is done.

    model = YOLO("models/yolo26s.pt") # now only this one work. to understand how to fine tune the doclayout yolo 

    train_size = 5
    val_size = 2

    pages = generate_train_and_validation_set(train_size=train_size, val_size=val_size, img_name="tft")

    # Fine tuning
    model.train(
        data="configs/data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        lr0=0.001,
        pretrained=True,
        freeze=10,
        device='cpu'
    )
