# KeyPoints
import cv2
import json
import os
import subprocess
import tempfile
import numpy as np
from matplotlib import pyplot as plt

def get_body_keypoints_with_visual(image_path, openpose_path="openpose"):
    """
    Runs OpenPose on the given image and returns both the keypoints (as JSON/dict)
    and an annotated image (numpy array) with the body structure drawn.
    
    Parameters:
      - image_path (str): Path to the input image.
      - openpose_path (str): Base path to the OpenPose directory.
      
    Returns:
      - keypoints (list): List of keypoints (2D pose) or None if extraction fails.
      - annotated_image (numpy.ndarray): Image with drawn keypoints and skeleton.
    """
    # Use temporary directories for isolated processing
    with tempfile.TemporaryDirectory() as temp_output:
        with tempfile.TemporaryDirectory() as temp_input:
            filename = os.path.basename(image_path)
            temp_image_path = os.path.join(temp_input, filename)
            # Copy image to temp input folder
            with open(image_path, "rb") as src, open(temp_image_path, "wb") as dst:
                dst.write(src.read())
            
            # Build and run OpenPose command
            cmd = [
                os.path.join(openpose_path, "build/examples/openpose/openpose.bin"),
                "--image_dir", temp_input,
                "--write_json", temp_output,
                "--display", "0",
                "--render_pose", "1",  # Enable rendering so it draws the pose on a blank background
                "--net_resolution", "-1x368"  # Example parameter; adjust as needed
            ]
            
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except subprocess.CalledProcessError as e:
                print("Error running OpenPose:", e)
                return None, None
            
            # Find JSON output file (for keypoints)
            json_files = [f for f in os.listdir(temp_output) if f.endswith(".json")]
            if not json_files:
                print("No JSON output found!")
                return None, None
            
            json_file_path = os.path.join(temp_output, json_files[0])
            with open(json_file_path, "r") as f:
                data = json.load(f)
            
            if "people" in data and len(data["people"]) > 0:
                keypoints = data["people"][0]["pose_keypoints_2d"]
            else:
                print("No keypoints detected!")
                return None, None
            
            # For the annotated image, OpenPose by default renders an image in the output folder
            # Look for a corresponding rendered image (commonly a file with the same name as the input image)
            rendered_files = [f for f in os.listdir(temp_input) if f.endswith(".png") or f.endswith(".jpg")]
            # Sometimes OpenPose outputs a rendered image in the same folder; otherwise, you might have to re-render
            # Here, we'll assume that if a rendered image was produced, it would be in the temp_input folder.
            annotated_image = None
            if rendered_files:
                rendered_image_path = os.path.join(temp_input, rendered_files[0])
                annotated_image = cv2.imread(rendered_image_path)
            else:
                # If no rendered image is found, we can draw the skeleton on a blank image manually.
                original_image = cv2.imread(image_path)
                annotated_image = draw_pose_on_image(original_image, keypoints)
            
            return keypoints, annotated_image

def draw_pose_on_black(image, keypoints, threshold=0.1):
    """
    Draws keypoints and skeleton on a blank (black) background, 
    using the given image dimensions and keypoints.
    
    :param image: numpy.ndarray of the original image (used for size).
    :param keypoints: list of keypoints (x1, y1, score1, x2, y2, score2, ...).
    :param threshold: Minimum confidence to draw a keypoint.
    :return: Annotated image (black background with drawn keypoints and skeleton).
    """
    # Create a black image of the same dimensions as the original image.
    h, w, _ = image.shape
    black_img = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Define pairs of keypoints to connect (skeleton structure).
    POSE_PAIRS = [
        (1, 2), (1, 5), (2, 3), (3, 4),
        (5, 6), (6, 7), (1, 8), (8, 9),
        (9, 10), (1, 11), (11, 12), (12, 13),
        (0, 14), (14, 16), (0, 15), (15, 17)
    ]
    
    n_points = int(len(keypoints) / 3)
    points = []
    
    # Compute the keypoint positions based on the image size.
    for i in range(n_points):
        x = int(keypoints[3 * i] * w)
        y = int(keypoints[3 * i + 1] * h)
        confidence = keypoints[3 * i + 2]
        if confidence > threshold:
            points.append((x, y))
            # Draw a green circle for each keypoint.
            cv2.circle(black_img, (x, y), 4, (0, 255, 0), -1)
        else:
            points.append(None)
    
    # Draw lines (skeleton) between keypoints.
    for pair in POSE_PAIRS:
        partFrom, partTo = pair
        if partFrom < len(points) and partTo < len(points):
            if points[partFrom] and points[partTo]:
                cv2.line(black_img, points[partFrom], points[partTo], (255, 0, 0), 2)
    
    return black_img

# Example usage:
if __name__ == "__main__":
    # Assuming 'original_img' is loaded and 'keypoints' are extracted
    original_img = cv2.imread("path/to/user_image.jpg")
    # For demonstration, assuming keypoints is a list of numbers:
    # [x1, y1, conf1, x2, y2, conf2, ...]
    keypoints = [0.5, 0.3, 0.9, 0.6, 0.4, 0.8, 0.7, 0.5, 0.85, 0.8, 0.6, 0.95]  # etc.
    annotated_black = draw_pose_on_black(original_img, keypoints)
    cv2.imshow("Annotated on Black", annotated_black)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
