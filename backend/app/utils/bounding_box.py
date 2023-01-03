import json

def get_data(distros_dict):
    yolo_output = []
    
    # For every frame.
    for distro in distros_dict:
        if len(distro['objects']) != 0:
            # For every detection.
            for obj in range(len(distro['objects'])):
                # Get values
                frame_id = distro['frame_id']
                class_id = distro['objects'][obj]["class_id"]
                
                x = distro['objects'][obj]["relative_coordinates"]["center_x"]
                y = distro['objects'][obj]["relative_coordinates"]["center_y"]
                width = distro['objects'][obj]["relative_coordinates"]["width"]
                height = distro['objects'][obj]["relative_coordinates"]["height"]
                
                confidence = distro['objects'][obj]["confidence"]
                
                yolo_output.append([frame_id, class_id, x, y, width, height, confidence])

    return yolo_output

def getBoundingBox(text_file_path):
    with open(text_file_path, 'r') as f:
        json_data = json.load(f)

    json_data = get_data(json_data)
    # [{frame_id} {class_id} {x} {y} {width} {height} {confidence}]
    return json_data
