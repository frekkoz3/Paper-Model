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
import cv2

if __name__ == "__main__":

    model = YOLO("models/first_try_ft_yolo26s.pt") # now only this one work. to understand how to fine tune the doclayout yolo 

    # Load image
    image_path = "imgs/proof.png"
    image = cv2.imread(image_path)

    # Run inference
    results = model(image)

    # Get annotated image (boxes + labels drawn)
    annotated = results[0].plot()

    # Show image
    cv2.imshow("Detections", annotated)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Save result
    cv2.imwrite("annotated.jpg", annotated)