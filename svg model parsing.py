import os
import json
import re
from bs4 import BeautifulSoup

#  Translation dictionary (define this separately or load from file)
translation = {
    "OH": "Living Room",
    "MH": "Bedroom",
    "K": "Kitchen",
    "ET": "Entry",
    "KH": "Bathroom",
    "WC": "Toilet",
    "VH": "Walk-in Closet",
    "TK": "Utility Room",
    "KHH": "Utility Room",
    "PKH": "Dressing Room",
    "KHH/PKH": "Utility / Dressing Room",
    "PH": "Washing Room",
    "RT": "Dining Area",
    "TERASSI": "Terrace",
    "KUISTI": "Porch",
    "TEKN": "Technical Room",
    "TEKN.TILA": "Technical Room",
    "VARASTO": "Storage",
    "VAR": "Storage",
    "VAR/": "Storage",
    "SAUNA": "Sauna",
    "S": "Sauna",
    "AULA": "Lobby",
    "AH": "Living Room/Lounge",
    "TYÖHUONE": "Office",
    "TYÖH/VERSTAT": "Office/Workshop",
    "TYÖ- JA VIERASH": "Office and Guest Room",
    "RUOKAILU": "Dining Area",
    "RUOK": "Dining",
    "RUOK.TILA": "Dining Area",
    "PARVEKE": "Balcony",
    "LASI-PARV": "Glazed Balcony",
    "LASITETTU": "Glazed Balcony/Terrace",
    "LASIKUISTI": "Glazed Porch",
    "ULKOTILA": "Outdoor Space",
    "KORKEA TILA": "High Ceiling Space",
    "KATT.H": "Ceiling Height Room",
    "H": "Generic Room",
    "R": "Generic Room",
    "UNDEFINED": "Unlabeled",
    "PE": "Mirror/Cabinet",
    "PESUH": "Laundry Room",
    "PESU": "Laundry/Washing Room",
    "PSH": "Shower",
    "KK": "Kitchenette",
    "KATOS": "Shelter/Shed",
    "SH": "Shower Room",
    "KEITTIÖ": "Kitchen",
    "AUTOKATOS": "Carport",
    "AUTOTALLI": "Garage",
    "AT": "Garage",
    "LIIKETILA": "Commercial Space",
    "ALKOVI": "Alcove",
    "SpaceForAppliance": "Appliance Space",
    "SpaceForAppliance2": "Appliance Space",
    "APUK": "Auxiliary Kitchen",
    "HARRASTUS": "Hobby Room",
    "HARRASTETILA": "Hobby Space",
    "TH": "Fireplace/Technical Room",
    "RP": "Fireplace",
    "KÄYTÄVÄ": "Corridor",
    "WC/KH": "Toilet/Bathroom",
    "WC/PH": "Toilet/Washing Room",
    "WC-PH": "Toilet-Washing Room",
    "KH/KHH": "Bathroom/Utility Room",
    "KOM": "Closet/Storage",
    "ULLAKKO": "Attic",
    "KYLMÄ VARASTOTILA": "Cold Storage",
    "KYLMÄ VAR.": "Cold Storage",
    "AVOK": "Open Kitchen",
    "PUUPATIO": "Wooden Patio",
    "NURMI PIHAA": "Grass Yard",
    "PSH": "Shower",
    "LÖYLYH": "Steam Room",
    "MEIKKIH": "Makeup Room",
    "KOTITEATTERI": "Home Theater",
    "SISÄVAR": "Indoor Storage",
    "ULKOVAR": "Outdoor Storage",
    "ÖLJY-POLTIN": "Oil Burner",
    "BAARIOS": "Bar Area",
    "AIDATTUA PUUTARHAA": "Fenced Garden",
    "PUUSEPÄN VERSTAS": "Carpenter’s Workshop",
    "TOIMISTOH.": "Office Room",
    "TERASSIPARVEKE": "Terrace Balcony",
    "KATTOTERASSI": "Roof Terrace",
    "MH\\KIRJASTO": "Bedroom/Library",
    "LASIT.PARVEKE": "Glazed Balcony",
    "PARVEKE LASITUS": "Glazed Balcony",
    "LASI PARVEKE": "Glazed Balcony",
    "LAS. PARVEKE": "Glazed Balcony",
    "KPH/": "Bathroom",
    "KPH/WC/KHH": "Bathroom/Toilet/Utility Room",
    "KPH/KHH": "Bathroom/Utility Room",
    "KPH/ASK.H": "Bathroom/Hobby Hall",
    "KPH/ÖLJY": "Bathroom/Fuel Storage",
    "KPH/TAKKA.H": "Bathroom/Fireplace Room",
    "KPH/TKH": "Bathroom/Fireplace Room",
    "KPH/SALI": "Bathroom/Recreation Room",
    "KPH/PARVI": "Bathroom/Loft",
    "KPH/VERANTA": "Bathroom/Porch",
    "KPH/HALLI": "Bathroom/Hall",
    "KPH/PIHA": "Bathroom/Yard",
    "KPH/Undefined": "Bathroom/Unlabeled",
    "KPH/TUPAK": "Bathroom/Fireplace Area",
    "KPH/TALOUS": "Bathroom/Utility",
    "KPH/KOMERO": "Bathroom/Closet",
    "KPH/KUIVAUSH": "Bathroom/Drying Room",
    "KPH/RT/MH": "Bathroom/Dining/Bedroom",
    "KPH/ETEISAULA": "Bathroom/Entry Lobby",
    "KPH/ARKIOLOH": "Bathroom/Living Area",
    "KPH/VIERASHUONE": "Bathroom/Guest Room",
    "KPH/PIHA/TERASSI": "Bathroom/Yard/Terrace",
    "KPH/PATIO": "Bathroom/Patio",
    "KPH/TV-H": "Bathroom/TV Room",
    "KPH/PYÖRÄT": "Bathroom/Bike Storage",
    "KPH/ULKOVARASTO": "Bathroom/Outdoor Storage",
    "KPH/MATALA VAR": "Bathroom/Low Storage",
    "KPH/VAR/TEKN": "Bathroom/Technical Storage",
    "KPH/TEKN+VAR": "Bathroom/Technical Storage",
    "KPH/K/RUOK": "Bathroom/Kitchen/Dining",
    "KPH/K+RT": "Bathroom/Kitchen/Dining Area",
    "KPH/K/RT": "Bathroom/Kitchen/Dining Area",
    "KPH/KATETTU TERASSI": "Bathroom/Glazed Terrace",
    "KPH/LASITETTU PARVEKE": "Bathroom/Glazed Balcony",
    "KPH/LASITETTU TERASSI": "Bathroom/Glazed Terrace",
    "KPH/AVOTERASSI": "Bathroom/Open Terrace",
    "KPH/SISÄPIHA": "Bathroom/Inner Yard",
    "KPH/TERASSIPIHA": "Bathroom/Terrace Yard",
    "KPH/PIHA": "Bathroom/Yard",
    "KPH/PIHA/TERASSI": "Bathroom/Yard/Terrace",
    "KPH/ULKOVAR": "Bathroom/Outdoor Storage",
    "KPH/VAR/KYLMÄ": "Bathroom/Cold Storage",
    "KPH/ALLAS": "Bathroom/Pool",
    "KPH/UIMA-ALLAS": "Bathroom/Swimming Pool",
    "KPH/BAARIOS": "Bathroom/Bar Area",
    "KPH/TV-H": "Bathroom/TV Room",
    "KPH/HISSI": "Bathroom/Elevator",
    "KPH/PYYKKI-H": "Bathroom/Laundry Hall",
    "KPH/PARV.": "Bathroom/Loft",
    "KPH/TUPA": "Bathroom/Cabin",
    "KPH/TUPA/PARVI": "Bathroom/Cabin/Loft",
    "KPH/KELLARI": "Bathroom/Basement",
    "KPH/KELLARI/KYLMÄ ULLAKKO": "Bathroom/Basement/Cold Attic",
    "KPH/KELLARI/TALOUS": "Bathroom/Basement/Utility",
    "KPH/KELLARI/ÖLJY": "Bathroom/Basement/Fuel Storage",
    "KPH/KELLARI/ASK": "Bathroom/Basement/Hobby Room",
    "KPH/KELLARI/HALLI": "Bathroom/Basement/Hall",
    "KPH/KELLARI/KATETTU TERASSI": "Bathroom/Basement/Glazed Terrace",
    "KPH/KELLARI/PUKUH": "Bathroom/Basement/Dressing Room",
    "KPH/KELLARI/PUUVAJA": "Bathroom/Basement/Wood Shed",
    "KPH/KELLARI/POLTTOAIH": "Bathroom/Basement/Fuel Storage",
    "KPH/KELLARI/ASK.H": "Bathroom/Basement/Hobby Hall",
    "KPH/KELLARI/PANNUH": "Bathroom/Basement/Boiler Room",
    "KPH/KELLARI/ÖLJY": "Bathroom/Basement/Fuel Storage",
    "KPH/KELLARI/PUUSEPÄN VERSTAS": "Bathroom/Basement/Workshop",
    "KPH/KELLARI/TOIMISTOH.": "Bathroom/Basement/Office Room",
    "KPH/KELLARI/SALI": "Bathroom/Basement/Recreation Room",
    "KPH/KELLARI/VAR/VH": "Bathroom/Basement/Storage/Dressing",
    "KPH/KELLARI/ARKIOLOH": "Bathroom/Basement/Living Area",
    "KPH/KELLARI/VIERASHUONE": "Bathroom/Basement/Guest Room",
    "KPH/KELLARI/Undefined": "Bathroom/Basement/Unlabeled",
}

label_groups = {
    # Living spaces
    "Living Room": "Living/Room",
    "Bedroom" : "Bedroom",
    "Kitchen" : "Kitchen",
    "Kitchenette" : "Kitchen",
    "Open Kitchen" : "Kitchen",
    "Dining" : "Dining",
    "Dining Area" : "Dining",
    "Entry/Hallway" : "Entry/Hallway",
    "Lobby": "Entry/Hallway",
    "TOilet" : "Toliet",
    "Living Room/Lounge": "Living/Room",
    "Bathroom": "Bathroom",
    "Bathroom/Utility Room": "Bathroom",
    "Bathroom/Toilet/Utility Room": "Bathroom",
    "Bathroom/Basement": "Bathroom",
    "Bathroom/Basement/Workshop": "Bathroom",
    "Bathroom/Basement/Utility": "Bathroom",
    "Bathroom/Basement/Fuel Storage": "Bathroom",
    "Bathroom/Basement/Guest Room": "Bathroom",
    "Bathroom/Basement/Storage/Dressing": "Bathroom",
    "Bathroom/Basement/Cold Attic": "Bathroom",
    "Bathroom/Basement/Office Room": "Bathroom",
    "Bathroom/Basement/Recreation Room": "Bathroom",
    "Bathroom/Basement/Living Area": "Bathroom",
    "Bathroom/Basement/Glazed Terrace": "Bathroom",
    "Bathroom/Basement/Hobby Room": "Bathroom",
    "Bathroom/Basement/Hobby Hall": "Bathroom",
    "Bathroom/Basement/Hall": "Bathroom",
    "Bathroom/Basement/Dressing Room": "Bathroom",
    "Bathroom/Basement/Wood Shed": "Bathroom",
    "Bathroom/Basement/Boiler Room": "Bathroom",
    "Bathroom/Basement/Unlabeled": "Bathroom",
    "Bathroom/Fireplace Room": "Bathroom",
    "Bathroom/Fireplace Area": "Bathroom",
    "Bathroom/Closet": "Bathroom",
    "Bathroom/Drying Room": "Bathroom",
    "Bathroom/Dining/Bedroom": "Bathroom",
    "Bathroom/Entry Lobby": "Bathroom",
    "Bathroom/Living Area": "Bathroom",
    "Bathroom/Guest Room": "Bathroom",
    "Bathroom/Yard/Terrace": "Bathroom",
    "Bathroom/Patio": "Bathroom",
    "Bathroom/TV Room": "Bathroom",
    "Bathroom/Bike Storage": "Bathroom",
    "Bathroom/Outdoor Storage": "Bathroom",
    "Bathroom/Low Storage": "Bathroom",
    "Bathroom/Technical Storage": "Bathroom",
    "Bathroom/Glazed Terrace": "Bathroom",
    "Bathroom/Open Terrace": "Bathroom",
    "Bathroom/Inner Yard": "Bathroom",
    "Bathroom/Terrace Yard": "Bathroom",
    "Bathroom/Yard": "Bathroom",
    "Bathroom/Cold Storage": "Bathroom",
    "Bathroom/Pool": "Bathroom",
    "Bathroom/Swimming Pool": "Bathroom",
    "Bathroom/Bar Area": "Bathroom",
    "Bathroom/Elevator": "Bathroom",
    "Bathroom/Laundry Hall": "Bathroom",
    "Bathroom/Loft": "Bathroom",
    "Bathroom/Cabin": "Bathroom",
    "Bathroom/Cabin/Loft": "Bathroom",
    "Bathroom/Unlabeled": "Bathroom",
    "Bedroom": "Bedroom",
    "Bedroom/Library": "Bedroom",
    "Kitchen": "Kitchen",
    "Kitchenette": "Kitchen",
    "Auxiliary Kitchen": "Kitchen",
    "Open Kitchen": "Kitchen",
    "Dining": "Dining",
    "Dining Area": "Dining",
    "Entry": "Entry/Hallway",
    "Entry Lobby": "Entry/Hallway",
    "Lobby": "Entry/Hallway",
    "Toilet": "Toilet",
    "Toilet/Bathroom": "Toilet",
    "Toilet/Washing Room": "Toilet",
    "Toilet-Washing Room": "Toilet",
    "Utility Room": "Utility",
    "Utility / Dressing Room": "Utility",
    "Bathroom/Utility": "Utility",
    "Walk-in Closet": "Closet",
    "Closet/Storage": "Closet",
    "Dressing Room": "Closet",
    "Washing Room": "Laundry",
    "Laundry Room": "Laundry",
    "Laundry/Washing Room": "Laundry",
    "Sauna": "Sauna",
    "Steam Room": "Sauna",
    "Shower": "Bathroom",
    "Shower Room": "Bathroom",
    "Fireplace": "Fireplace",
    "Fireplace/Technical Room": "Fireplace",
    "Garage": "Garage/Carport",
    "Carport": "Garage/Carport",
    "Terrace": "Balcony/Terrace",
    "Terrace Balcony": "Balcony/Terrace",
    "Roof Terrace": "Balcony/Terrace",
    "Glazed Balcony": "Balcony/Terrace",
    "Glazed Balcony/Terrace": "Balcony/Terrace",
    "Glazed Porch": "Balcony/Terrace",
    "Porch": "Balcony/Terrace",
    "Balcony": "Balcony/Terrace",
    "Storage": "Storage",
    "Cold Storage": "Storage",
    "Indoor Storage": "Storage",
    "Outdoor Storage": "Storage",
    "Office": "Office",
    "Office Room": "Office",
    "Office/Workshop": "Office",
    "Office and Guest Room": "Office",
    "Guest Room": "Bedroom",
    "Corridor": "Entry/Hallway",
    "Attic": "Storage",
    "Appliance Space": "Utility",
    "Hobby Room": "Recreation",
    "Hobby Space": "Recreation",
    "Mirror/Cabinet": "Utility",
    "Shelter/Shed": "Storage",
    "Commercial Space": "Commercial",
    "Alcove": "Bedroom",
    "Wooden Patio": "Balcony/Terrace",
    "Grass Yard": "Outdoor Space",
    "Home Theater": "Recreation",
    "Makeup Room": "Utility",
    "Oil Burner": "Utility",
    "Bar Area": "Recreation",
    "Fenced Garden": "Outdoor Space",
    "Ceiling Height Room": "Generic Room",
    "High Ceiling Space": "Generic Room",
    "Generic Room": "Generic Room",
    "Unlabeled": "Unlabeled"
}

# Step 3: Translation + Grouping function
def normalize_and_group(label):
    if not label or not isinstance(label, str):
        return "Unlabeled"
    label = label.strip().upper()
    translated = translation.get(label, label)
    grouped = label_groups.get(translated, translated)
    return grouped

#  Label normalization
def normalize_label(label):
    label = label.upper().strip()
    label = re.sub(r"[^\w\s/\\+.-]", "", label)
    label = label.replace("\\", "/").replace("+", "/").replace("-", " ")
    parts = re.split(r"[ /]", label)
    translated_parts = [translation.get(part, part) for part in parts if part]
    normalized_parts = []
    for part in translated_parts:
        part = re.sub(r"[^\w\s/\\+.-]", "", part)
        part = part.replace("\\", "/").replace("+", "/").replace("-", " ")
        normalized_parts.extend(re.split(r"[ /]", part))
    return "/".join([p for p in normalized_parts if p])

# Category map
unique_categories = sorted(set(normalize_label(key) for key in translation.keys()))
category_map = {label: idx + 1 for idx, label in enumerate(unique_categories)}
category_lookup = {idx + 1: label for idx, label in enumerate(unique_categories)}

#  SVG loader
def extract_svg_root(svg_path):
    with open(svg_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, "xml")
    return soup.find("svg")

#  Bounding box parser
def parse_polygon_bbox(polygon):
    points = polygon.get("points", "")
    coords = [tuple(map(float, p.split(","))) for p in points.strip().split()]
    xs, ys = zip(*coords)
    x, y, w, h = min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)
    return [x, y, w, h]

#  Room parser
def parse_rooms(svg_root):
    rooms = []
    unmapped_labels = set()
    for g in svg_root.find_all("g", class_=lambda c: c and "Space" in c):
        polygon = g.find("polygon")
        if not polygon:
            continue

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
        if normalized_label not in category_map:
            unmapped_labels.add(normalized_label)
            continue

        bbox = parse_polygon_bbox(polygon)
        rooms.append({
            "name": normalized_label,
            "bbox": bbox
        })

    if unmapped_labels:
        print(f" Unmapped labels: {unmapped_labels}")
    return rooms

#  COCO annotation generator
def generate_annotations(rooms, image_id, category_map, start_id=1, label_grouping=None):
    annotations = []
    for i, room in enumerate(rooms):
        name = room["name"]
        if name in category_map:
            category_id = category_map[name]
            area = room["bbox"][2] * room["bbox"][3]
            annotations.append({
                "id": start_id + i,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": room["bbox"],
                "area": area,
                "iscrowd": 0
            })
    return annotations

#  Folder processor
def process_svg_folder(folder_path, output_json):
    images = []
    annotations = []
    image_id = 1000
    ann_id = 1

    for filename in os.listdir(folder_path):
        if not filename.endswith(".svg"):
            continue

        svg_path = os.path.join(folder_path, filename)
        svg_root = extract_svg_root(svg_path)
        rooms = parse_rooms(svg_root)

        images.append({
            "id": image_id,
            "file_name": filename,
            "width": 2048,
            "height": 2048
        })

        anns = generate_annotations(rooms, image_id, category_map, start_id=ann_id)
        annotations.extend(anns)
        ann_id += len(anns)
        image_id += 1

    coco_data = {
        "images": images,
        "annotations": annotations,
        "categories": [{"id": cid, "name": name} for name, cid in category_map.items()]
    }

    with open(output_json, "w") as f:
        json.dump(coco_data, f, indent=2)
    print(f" Saved {output_json} with {len(images)} images and {len(annotations)} annotations.")
