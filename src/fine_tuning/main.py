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
from src.generator.data_gen import generate_train_and_validation_set
from src.utils import clean_folder # needed if we want to clean the folder after the training

if __name__ == '__main__':

    # This is a simple fine tuning routine for a yolo26 model
    # trying the doclayout-yolo model could be good
    # This is not complete. Augmentation should be included. 

    model = YOLO("models/yolo26s.pt") # now only this one work. to understand how to fine tune the doclayout yolo 

    # Fine tuning
    model.train(
        data="configs/data.yaml",
        epochs=50,
        imgsz=640,
        batch=16,
        lr0=0.001,
        pretrained=True,
        freeze=10,
        device='cuda'
    )

    model.save("models/first_try_ft_yolo26.pt")
