base_dir = "/content/cubicasa_dataset/cubicasa5k"

def process_split(split_name, folder_paths, output_json, label_grouping=None):
    images, annotations = [], []
    image_id, ann_id = 1000, 1
    present_categories = set()

    if 'category_map' not in globals():
        print("Error: category_map not found. Please run the data processing cell first.")
        return

    category_lookup = {cid: name for name, cid in category_map.items()}

    for relative_path in folder_paths:
        svg_path = os.path.join(base_dir, relative_path, "model.svg")
        png_path = os.path.join(base_dir, relative_path, "F1_scaled.png")

        if not os.path.exists(svg_path):
            print(f" model.svg not found at {svg_path}")
            continue
        if not os.path.exists(png_path):
            print(f" F1_scaled.png not found at {png_path}")
            continue

        try:
            from PIL import Image
            with Image.open(png_path) as img:
                width, height = img.size
        except Exception as e:
            print(f" Could not read image size for {png_path}: {e}")
            continue

        svg_root = extract_svg_root(svg_path)
        rooms = parse_rooms(svg_root)

        style = relative_path.split("/")[0]
        folder_name = relative_path.split("/")[1]

        images.append({
            "id": image_id,
            "file_name": png_path,
            "style": style,
            "width": width,
            "height": height
        })

        anns = generate_annotations(rooms, image_id, category_map, start_id=ann_id, label_grouping=label_grouping)
        annotations.extend(anns)
        ann_id += len(anns)
        image_id += 1

        for ann in anns:
            if ann["category_id"] in category_lookup:
                present_categories.add(category_lookup[ann["category_id"]])
            else:
                print(f" Category ID {ann['category_id']} not found in category_lookup.")

    categories_list = [{"id": cid, "name": name} for name, cid in category_map.items()]

    coco_data = {
        "images": images,
        "annotations": annotations,
        "categories": categories_list
    }

    os.makedirs(os.path.dirname(output_json), exist_ok=True)
    with open(output_json, "w") as f:
        json.dump(coco_data, f, indent=2)
    print(f" Saved {split_name} annotations to {output_json}")
