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

# classes for the model
# 1 -> header 
# 2 -> footer
# 3 -> column
# 4 -> advertisement
# these should be sufficient since we want to handle patches later on

from src.generator.page import Page, generate_random_page
import cv2 # needed to visualize the rendering

class YOLOAnnotator:

    def __init__(self, page : Page):
        self.page = page

    def exctract_YOLOv10_annotations(self):
        h_annotation = f"{self.page.header.get_YOLO_annotation(class_id=0)}\n" if self.page.header else ""
        f_annotation = f"{self.page.footer.get_YOLO_annotation(class_id=2)}\n" if self.page.footer else ""
        s_annotations = ""
        for section in self.page.sections:
            s_annotations+=f"{section.get_YOLO_annotation(class_id=1)}\n"
        return "".join([h_annotation, f_annotation, s_annotations])

if __name__ == '__main__':

    page = generate_random_page()

    annotator = YOLOAnnotator(page)
    labels = annotator.exctract_YOLOv10_annotations()
    image_path = "output/debug.jpg"
    
    img = cv2.imread(image_path)
    h, w = img.shape[:2]

    for label in labels.split("\n"):
        try:        
            cls, x_c, y_c, bw, bh = map(float, label.strip().split())

            # YOLO normalized → pixel coords
            x_c *= w
            y_c *= h
            bw *= w
            bh *= h

            x1 = int(x_c - bw / 2)
            y1 = int(y_c - bh / 2)
            x2 = int(x_c + bw / 2)
            y2 = int(y_c + bh / 2)

            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, str(int(cls)), (x1, y1 - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        except Exception as e:
            print(label)

    cv2.namedWindow("YOLO visualization", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("YOLO visualization", 800, 600)

    cv2.imshow("YOLO visualization", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()