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
from src.generator.page import generate_random_page
from src.annotator.extractor import YOLOAnnotator

from pathlib import Path

def save_yolo_labels(label_path, annotations : str):
    """
    annotations: str where each line is a yolo annotation
    values must already be normalized [0,1]
    """
    with open(label_path, "w") as f:
        for ann in annotations.split("\n"):
            try:
                class_id, x, y, w, h = ann.split()
                f.write(f"{class_id} {x} {y} {w} {h}\n")
            except Exception as e:
                pass

if __name__ == '__main__':

    # This is a simple fine tuning routine for a doclayout-yolo model
    # This is not complete. Augmentation should be included. 
    # Also parallelization of the generation process.
    # And deletion of the artifacts once the training is done.

    model = YOLO("models/yolo26s.pt") # now only this one work. to understand how to fine tune the doclayout yolo 

    base_path = Path("data")

    train_img_path = base_path / "images/train"
    train_lbl_path = base_path / "labels/train"

    val_img_path = base_path / "images/val"
    val_lbl_path = base_path / "labels/val"

    # Create folders if they don't exist
    train_img_path.mkdir(parents=True, exist_ok=True)
    train_lbl_path.mkdir(parents=True, exist_ok=True)
    val_img_path.mkdir(parents=True, exist_ok=True)
    val_lbl_path.mkdir(parents=True, exist_ok=True)

    """
    img_name = f"debug_"
    img_path = train_img_path / img_name

    # here generated
    pages = generate_random_page(save_jpg=True, o_path=str(img_path), n_images=20)

    # Train set
    for i in range(5):
        img_name = f"debug_{i}.jpg"
        img_path = train_img_path / img_name

        extractor = YOLOAnnotator(pages[i])
        annotations = extractor.exctract_YOLO_annotations()

        label_path = train_lbl_path / f"debug_{i}.txt"

        save_yolo_labels(label_path, annotations)
    

    img_name = f"val_"
    img_path = val_img_path / img_name

    # here generated
    pages = generate_random_page(save_jpg=True, o_path=str(img_path), n_images=5)

    # Validation Set
    for i in range(5):
        img_name = f"val_{i}.jpg"
        img_path = val_img_path / img_name

        extractor = YOLOAnnotator(pages[i])
        annotations = extractor.exctract_YOLO_annotations()

        label_path = val_lbl_path / f"val_{i}.txt"

        save_yolo_labels(label_path, annotations)
    
    """
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
