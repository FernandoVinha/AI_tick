import os
import xml.etree.ElementTree as ET

# Path to the directories where the XML files are located
dataset_path = '/'  # Update to your path
folders = ['train', 'val']

# List of classes
classes = ['tick']

# Function to convert bounding box coordinates
def convert(size, box):
    dw = 1. / size[0]  # Calculate width normalization factor
    dh = 1. / size[1]  # Calculate height normalization factor
    x = (box[0] + box[1]) / 2.0 - 1  # Calculate center x coordinate
    y = (box[2] + box[3]) / 2.0 - 1  # Calculate center y coordinate
    w = box[1] - box[0]  # Calculate box width
    h = box[3] - box[2]  # Calculate box height
    x = x * dw  # Normalize x
    w = w * dw  # Normalize width
    y = y * dh  # Normalize y
    h = h * dh  # Normalize height
    return (x, y, w, h)

# Function to convert annotation from XML to TXT
def convert_annotation(folder, image_id):
    # Open the XML file and corresponding output text file
    in_file = open(f'{dataset_path}/{folder}/{image_id}.xml')
    out_file = open(f'{dataset_path}/{folder}/{image_id}.txt', 'w')
    
    # Parse the XML file
    tree = ET.parse(in_file)
    root = tree.getroot()
    
    # Get image size (width and height)
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    # Iterate through each object in the XML
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text  # Check if object is difficult
        cls = obj.find('name').text  # Get class name
        if cls not in classes or int(difficult) == 1:  # Skip if class not in list or difficult
            continue
        cls_id = classes.index(cls)  # Get class ID
        xmlbox = obj.find('bndbox')  # Get bounding box coordinates
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
             float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)  # Convert to normalized coordinates
        out_file.write(f"{cls_id} " + " ".join([str(a) for a in bb]) + '\n')  # Write to output file

# Iterate through the folders and files to convert all XML files
for folder in folders:
    for filename in os.listdir(f'{dataset_path}/{folder}'):
        if filename.endswith('.xml'):  # Process only XML files
            image_id = os.path.splitext(filename)[0]  # Get image ID
            convert_annotation(folder, image_id)  # Convert annotations
