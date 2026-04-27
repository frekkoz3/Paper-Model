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
import cv2
import numpy as np
import random

def ink_flip(img, threshold=245, p=0.1):
    mask = (img < threshold).any(axis=2)

    # Generate flip mask (same spatial size)
    flip = np.random.rand(img.shape[0], img.shape[1]) < p

    # Apply only where both masks are true
    combined_mask = mask & flip

    noisy_img = img.copy()
    noisy_img[combined_mask] = 255

    return noisy_img

def augment_page(img_path: str = "output/debug.jpg", l_path: str = "output/debug.txt"):
    """
    Augment a newspaper page and update its YOLO annotations accordingly.

    The augmented image and annotations overwrite the originals.

    YOLO annotation format:
        class_id x_center y_center width height

    Coordinates are normalized w.r.t. the full image size.

    Class mapping:
        0 -> Header
        1 -> Section
        2 -> Section Title
        3 -> Column
        4 -> Banner
        5 -> Footer

    Applied augmentations:
        - Add random white margins (annotations adjusted)
        - Add ink-like noise inside content
        - Add noise in margins (lines/dots) -> TO IMPLEMENT
        - Small rotation (+-0.8°, annotations unchanged)

    Parameters
    ----------
    img_path : str
        Path to the input image.
    l_path : str
        Path to the YOLO annotation file.

    Returns
    -------
    None
        The function overwrites the image and annotation file.
    """

    annotations = []
    with open(l_path, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                annotations.append(list(map(float, line.split())))

    img = cv2.imread(img_path)
    if img is None:
        raise ValueError(f"Could not read image at {img_path}")

    h, w, _ = img.shape

    boxes = []
    for ann in annotations:
        class_id, x_center, y_center, bw, bh = ann

        x_center *= w
        y_center *= h
        bw *= w
        bh *= h

        x1 = int(x_center - bw / 2)
        y1 = int(y_center - bh / 2)
        x2 = int(x_center + bw / 2)
        y2 = int(y_center + bh / 2)

        boxes.append([class_id, x1, y1, x2, y2])

    # Ink flip noise
    img = ink_flip(img)

    # White margins
    top = random.randint(0, 80)
    bottom = random.randint(0, 80)
    left = random.randint(0, 80)
    right = random.randint(0, 80)

    img = cv2.copyMakeBorder(
        img, top, bottom, left, right,
        borderType=cv2.BORDER_CONSTANT,
        value=[255, 255, 255]
    )

    new_boxes = []
    for class_id, x1, y1, x2, y2 in boxes:
        new_boxes.append([
            class_id,
            x1 + left,
            y1 + top,
            x2 + left,
            y2 + top
        ])

    boxes = new_boxes
    h, w, _ = img.shape

    # Rotation
    angle = random.uniform(-0.8, 0.8)
    center = (w // 2, h // 2)

    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    img = cv2.warpAffine(
        img, M, (w, h),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )

    yolo_annotations = []
    for class_id, x1, y1, x2, y2 in boxes:
        x_center = (x1 + x2) / 2 / w
        y_center = (y1 + y2) / 2 / h
        bw = (x2 - x1) / w
        bh = (y2 - y1) / h

        yolo_annotations.append(
            f"{int(class_id)} {x_center:.6f} {y_center:.6f} {bw:.6f} {bh:.6f}"
        )

    cv2.imwrite(img_path, img)

    with open(l_path, "w") as file:
        for line in yolo_annotations:
            file.write(line + "\n")

if __name__ == '__main__':
    augment_page()