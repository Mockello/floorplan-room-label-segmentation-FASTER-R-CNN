from PIL import Image, ImageFile
import os
import json

# Increase Pillow's image size limit to handle large images
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

# Load split folders
train_folders = load_split_folders("/content/cubicasa_dataset/cubicasa5k/train.txt")
val_folders = load_split_folders("/content/cubicasa_dataset/cubicasa5k/val.txt")
test_folders = load_split_folders("/content/cubicasa_dataset/cubicasa5k/test.txt")

# Collect all normalized labels from translation keys
all_room_names_from_translation_keys = set(normalize_label(key) for key in translation.keys())

# Collect all normalized labels found in dataset
all_normalized_labels_in_dataset = set()
for split_folders in [train_folders, val_folders, test_folders]:
    for relative_path in split_folders:
        svg_path = os.path.join("/content/cubicasa_dataset/cubicasa5k", relative_path, "model.svg")
        if os.path.exists(svg_path):
            svg_root = extract_svg_root(svg_path)
            for g in svg_root.find_all("g", class_=lambda c: c and "Space" in c):
                label = None
                for sub in g.find_all("g", class_=lambda c: c and "NameLabel" in c):
                    text_tag = sub.find("text")
                    if text_tag and text_tag.text:
                        label = text_tag.text.strip()
                        break
                if not label:
                    label = g.get("inkscape:label") or g.get("id")
                    if label and "room-" in label:
                        label = label.split("room-")[-1].strip()
                if not label:
                    class_attr = g.get("class", "")
                    label = class_attr.split()[-1]
                normalized_label = normalize_label(label)
                all_normalized_labels_in_dataset.add(normalized_label)

# ✅ Mandatory Fix: Use zero-based indexing for category_id
unique_categories = sorted(list(all_room_names_from_translation_keys))
category_map = {name: idx for idx, name in enumerate(unique_categories)}
category_lookup = {idx: name for idx, name in enumerate(unique_categories)}

# Print audit info
print("\nUnique Normalized Labels found in the Dataset:")
for label in sorted(all_normalized_labels_in_dataset):
    print(label)

unmapped_labels_in_dataset = sorted(list(all_normalized_labels_in_dataset - set(category_map.keys())))
if unmapped_labels_in_dataset:
    print("\nLabels found in dataset but not in category_map (need translation/mapping):")
    for label in unmapped_labels_in_dataset:
        print(label)
else:
    print("\nAll normalized labels found in the dataset are in the category_map.")

# Generate annotations
process_split("train", train_folders, "annotations/train_annotations.json")
process_split("val", val_folders, "annotations/val_annotations.json")
process_split("test", test_folders, "annotations/test_annotations.json")
