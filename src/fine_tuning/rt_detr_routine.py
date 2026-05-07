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
from ultralytics import RTDETR

if __name__ == '__main__':

    # This is a vision model with a cnn backbone and a vision-transformer core
    # that should be able to better understand global relationship between different areas
    # Since it is always from ultralytics it is very easy to use

    model = RTDETR("models/rtdetr-l.pt")

    model.train(
        data="configs/data.yaml",
        epochs=100,
        imgsz=1024,
        batch=16,
        lr0=0.001,
        pretrained=True,
        freeze=10,
        device='cuda',
        workers=4
    )

    # resolution_number_modelname.pt
    model.save("models/1024_3_rt_detr.pt")