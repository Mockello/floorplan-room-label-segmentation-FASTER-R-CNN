from detectron2.engine import DefaultTrainer
from detectron2.config import get_cfg
from detectron2 import model_zoo
from detectron2.data.datasets import register_coco_instances
import os

#  Use zero-based category_map keys as thing_classes
thing_classes = sorted(category_map, key=lambda k: category_map[k])  # Sorted by category_id

#  Define paths
image_root = "/content/"  # Root directory where images are located
annotation_dir = "annotations"

#  Register datasets
register_coco_instances(
    "cubicasa_train",
    {"thing_classes": thing_classes},
    os.path.join(annotation_dir, "train_annotations.json"),
    image_root
)

register_coco_instances(
    "cubicasa_val",
    {"thing_classes": thing_classes},
    os.path.join(annotation_dir, "val_annotations.json"),
    image_root
)

register_coco_instances(
    "cubicasa_test",
    {"thing_classes": thing_classes},
    os.path.join(annotation_dir, "test_annotations.json"),
    image_root
)

#  Explicitly set thing_classes for robustness
MetadataCatalog.get("cubicasa_train").thing_classes = thing_classes
MetadataCatalog.get("cubicasa_val").thing_classes = thing_classes
MetadataCatalog.get("cubicasa_test").thing_classes = thing_classes
# Define output directory inside Drive
drive_output_dir = "/content/drive/My Drive/cubicasa_checkpoints"
os.makedirs(drive_output_dir, exist_ok=True)

# Use the correct number of classes from your dense category_map
NUM_CLASSES = len(category_map)

#  Set up configuration
cfg = get_cfg()
cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))

cfg.DATASETS.TRAIN = ("cubicasa_train",)
cfg.DATASETS.TEST = ("cubicasa_val",)
cfg.DATALOADER.NUM_WORKERS = 2
cfg.MODEL.DEVICE = "cpu"

cfg.MODEL.WEIGHTS = "/content/drive/MyDrive/cubicasa_checkpoints/model_0000999.pth"
cfg.SOLVER.IMS_PER_BATCH = 2
cfg.SOLVER.BASE_LR = 0.00025
cfg.SOLVER.MAX_ITER = 1000
cfg.SOLVER.STEPS = []  # No LR decay
cfg.SOLVER.CHECKPOINT_PERIOD = 100

cfg.MODEL.ROI_HEADS.BATCH_SIZE_PER_IMAGE = 128
cfg.MODEL.ROI_HEADS.NUM_CLASSES = NUM_CLASSES

cfg.OUTPUT_DIR = drive_output_dir

#  Start training
trainer = DefaultTrainer(cfg)
trainer.resume_or_load(resume=True)
trainer.train()
