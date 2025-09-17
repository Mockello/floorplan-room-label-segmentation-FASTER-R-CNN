from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
import random
import cv2
import os
import matplotlib.pyplot as plt

# Ensure category_map is available globally
if 'category_map' not in globals():
    print("Error: category_map not found. Please run the data processing cell first.")
else:
    # Set up configuration for inference
    cfg = get_cfg()
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))

    # Use the correct number of classes from your dense category_map
    NUM_CLASSES = len(category_map)
    cfg.MODEL.ROI_HEADS.NUM_CLASSES = NUM_CLASSES

    # Set the output directory to load the trained model
    cfg.OUTPUT_DIR = "/content/drive/My Drive/cubicasa_checkpoints"

    # Set the threshold for detections
    cfg.MODEL.RETINANET.SCORE_THRESH_TEST = 0.2
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.2

    # Load the latest checkpoint
    cfg.MODEL.WEIGHTS = os.path.join(cfg.OUTPUT_DIR, "model_final.pth")
    cfg.MODEL.DEVICE = "cpu"

    # Create predictor
    predictor = DefaultPredictor(cfg)

    # Load the validation dataset dictionaries
    val_annotation_file = "annotations/val_annotations.json"
    try:
        val_dataset_dicts = load_coco_json(val_annotation_file, "/content/")
    except FileNotFoundError:
        print(f"Error: Annotation file not found at {val_annotation_file}")
        val_dataset_dicts = []

    if val_dataset_dicts:
        # Pick a random image from the validation set
        sample_val = random.choice(val_dataset_dicts)
        img_path_val = sample_val["file_name"]

        # Load image safely
        img_val = cv2.imread(img_path_val)
        if img_val is None:
            print(f"⚠️ Image not found or unreadable: {img_path_val}")
        else:
            # Perform inference
            outputs = predictor(img_val)

            # Create metadata manually for visualization
            metadata_val = Metadata()
            metadata_val.thing_classes = list(category_map.keys())

            # Visualize the results
            v = Visualizer(img_val[:, :, ::-1], metadata=metadata_val, scale=1.0)
            out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
            plt.figure(figsize=(12, 12))
            plt.imshow(out.get_image())
            plt.axis('off')
            plt.title(f"Inference Results: {os.path.basename(img_path_val)}")
            plt.show()
    else:
        print("No validation dataset dictionaries loaded for inference.")
