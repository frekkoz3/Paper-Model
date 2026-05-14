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
from huggingface_hub import upload_file

if __name__ == '__main__':

    # This is a simple fine tuning routine for a yolo26 model
    # trying the doclayout-yolo model could be good
    # This is not complete. Augmentation should be included. 

    model = YOLO("models/yolo26s.pt") # now only this one work. to understand how to fine tune the doclayout yolo 

    # Fine tuning
    model.train(
        data="configs/data.yaml",
        epochs=100,
        imgsz=1024,
        batch=8,
        lr0=0.0001,
        lrf=0.00001,
        pretrained=True,
        freeze=10,
        device='cuda',
        workers=4
    )

    name = "1024_0_v3_yolo26.pt"
    local_path = f"models/{name}"
    # resolution_number_datasetversion_modelname.pt
    model.save(local_path)

    repo_id = "frekko/paper_model_yolo26"

    upload_file(
        path_or_fileobj=local_path,
        path_in_repo=name,
        repo_id=repo_id,
    )
