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

load_dotenv()

from ultralytics import YOLO, RTDETR
import cv2

from huggingface_hub import hf_hub_download

if __name__ == "__main__":

    using_yolo = False

    repo_id = "frekko/paper_model_yolo26" if using_yolo else "frekko/paper_model_rt_detr"
    model_name = "1024_0_v2_yolo26.pt" if using_yolo else "1024_0_v3_rt_detr.pt"

    model_path = hf_hub_download(
        repo_id=repo_id,
        filename=model_name,
        token=True
    )

    model = YOLO(model_path) if using_yolo else RTDETR(model_path)

    # Load image
    image_name = "piccolo_proof.png"
    image_path = f"imgs/{image_name}"
    image = cv2.imread(image_path)

    # Run inference
    results = model(image)

    # Get annotated image (boxes + labels drawn)
    annotated = results[0].plot()

    # Save result
    cv2.imwrite(f"imgs/{model_name}_annotated_{image_name}", annotated)