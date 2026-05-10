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
from ultralytics import YOLO, RTDETR
import cv2

if __name__ == "__main__":

    model_name = "1024_2_yolo26"

    model = YOLO(f"models/{model_name}.pt") # now only this one work. to understand how to fine tune the doclayout yolo 
    #model = RTDETR("models/first_try_ft_rt_detr.pt")
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