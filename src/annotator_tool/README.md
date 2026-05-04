# YOLO Annotation Tool

A lightweight Tkinter-based image annotation tool for creating YOLO-format bounding box datasets.

---

## Features

* Multi-image annotation workflow
* YOLO `.txt` annotation export
* Automatic annotation reload
* Zoom and pan support
* Scalable annotations
* Multiple label classes
* Undo and delete annotations
* Previous/Next image navigation
* Keyboard shortcuts for labels
* Original image resolution preserved
* Dashed rectangle live preview while drawing

---

## Labels

| ID | Label         |
| -- | ------------- |
| 0  | Header        |
| 1  | Section       |
| 2  | Section Title |
| 3  | Column        |
| 4  | Banner        |
| 5  | Footer        |

---

## Installation

### Stand alone Requirements

```bash
pip install pillow
```

Tkinter is included with most Python installations.

---

## Usage

Run the tool:

```bash
python annotator.py
```

Then:

1. Click `Open Images`
2. Select one or multiple images
3. Choose a label from the side panel
4. Draw bounding boxes with the mouse
5. Use `Next` / `Previous` to navigate images
6. Annotations are saved in YOLO format automatically

---

## Controls

### Mouse

| Action             | Description     |
| ------------------ | --------------- |
| Left Click + Drag  | Draw annotation |
| Right Click + Drag | Pan image       |
| Mouse Wheel        | Zoom in/out     |

---

### Keyboard

| Key      | Action                     |
| -------- | -------------------------- |
| 0-5      | Select label               |
| Delete   | Delete selected annotation |
| Ctrl + Z | Undo last annotation       |

---

## YOLO Output Format

Each image generates a `.txt` file with the same name:

```text
image.jpg
image.txt
```

YOLO annotation format:

```text
class_id x_center y_center width height
```

Coordinates are normalized between `0` and `1`.

Example:

```text
0 0.512300 0.082100 0.921100 0.101200
```
