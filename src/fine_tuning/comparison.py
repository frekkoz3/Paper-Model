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
# This script demonstrates the extent of distortion introduced by YOLO when applied to high-quality scan of newspaper page images.

import cv2
import matplotlib.pyplot as plt

#img_path = "imgs/proof.png" # whole page
# img_path = "imgs/column_proof.png" # single column
img_path = "imgs/column_patch_proof.png" # squared patch on a single column

img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# YOLO-style resize
yolo_size = 960
resized = cv2.resize(img, (yolo_size, yolo_size))

fig, axs = plt.subplots(2, figsize=(10, 10))

axs[0].imshow(img)
axs[0].set_title(f"Original ({img.shape[1]}x{img.shape[0]})")
axs[0].axis("off")

axs[1].imshow(resized)
axs[1].set_title(f"Resized to ({yolo_size}x{yolo_size})")
axs[1].axis("off")

plt.tight_layout()
plt.show()
