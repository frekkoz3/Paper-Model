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
from dotenv import load_dotenv
import os

load_dotenv()

from ultralytics import RTDETR
from huggingface_hub import login, upload_file

login(token=os.environ["HF_TOKEN"])

if __name__ == '__main__':

    # This is a vision model with a cnn backbone and a vision-transformer core
    # that should be able to better understand global relationship between different areas
    # Since it is always from ultralytics it is very easy to use

    model = RTDETR("models/rtdetr-l.pt")

    model.train(
        data="configs/data.yaml",
        epochs=60,
        imgsz=1024,
        batch=16,
        lr0=0.0001,
        lrf=0.00001,
        pretrained=True,
        freeze=10,
        device='cuda',
        workers=4
    )

    name = "1024_0_v3_rt_detr.pt"
    local_path = f"models/{name}"
    # resolution_number_datasetversion_modelname.pt
    model.save(local_path)

    repo_id = "frekko/paper_model_rt_detr"

    upload_file(
        path_or_fileobj=local_path,
        path_in_repo=name,
        repo_id=repo_id,
    )