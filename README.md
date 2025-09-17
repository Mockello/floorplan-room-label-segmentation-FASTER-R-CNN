# Faster R-CNN model for room label detection in floorplan images using Detectron2

This project focuses on detecting **room labels** in architectural floorplans using Faster R-CNN implemented via Detectron2. The goal is to automate semantic region recognition to support digital workflows in real estate, interior design, and spatial analytics.

---

## 📌 Project Objective

Architectural floorplans contain rich semantic information, but manual interpretation of room labels is slow and error-prone. This project builds a robust object detection pipeline to identify room labels from floorplan images, enabling:

- Faster semantic parsing of architectural layouts  
- Improved accuracy in room classification and zoning  
- Scalable integration into downstream planning or analytics tools

---

## 🧩 Core Workflow

### Data Preparation
- Floorplan images annotated in COCO format  
- Focused on room label regions with bounding boxes and category IDs  
- Supports multilingual labels (e.g., "Kitchen", "Baño", "トイレ")

### Model Training
- Trained a Faster R-CNN model using Detectron2  
- Leveraged GPU acceleration via Google Colab  
- Tuned hyperparameters for domain-specific performance

### Inference & Visualization
- Ran predictions on unseen test images  
- Visualized bounding boxes over room label regions  
- Saved outputs for qualitative review

### Evaluation
- Measured performance using COCO metrics  
- Focused on Average Precision (AP) for room label detection  
- Validated consistency across varied floorplan styles and languages

---

## 🏗 Tech Stack

- **Framework**: Detectron2  
- **Language**: Python 3.11  
- **Libraries**: PyTorch, OpenCV, Matplotlib, pycocotools  
- **Environment**: Google Colab (GPU-accelerated training)

---

## 📊 Results

- The trained model demonstrates high accuracy in detecting room labels  
- Visual outputs show precise bounding boxes aligned with label text  
- Evaluation metrics confirm robust generalization across test samples

---

## 🔑 Key Learnings

- How to prepare a custom COCO dataset for semantic architectural analysis  
- Training object detection models on non-natural image domains  
- Using COCO AP metrics to evaluate label detection  
- Building an end-to-end pipeline from annotation to inference

---

##  Repository Contents


---

##  Getting Started

```bash
pip install -r requirements.txt

## Training
python train.py --data_dir path/to/train_data --epochs 50

## Inference
python inference.py --input path/to/image.png --output results/output.png
