# KeyPoints
import json
import os
import subprocess


def get_body_keypoints(image_path, openpose_path="openpose"):
    """
    Runs OpenPose on the given image and extracts body keypoints.

    Parameters:
    - image_path (str): Path to the input image.
    - openpose_path (str): Path to the OpenPose binary (default: "openpose").

    Returns:
    - list: List of extracted keypoints (2D pose).
    """

    # Ensure output directory exists
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)

    # Run OpenPose command
    cmd = [
        openpose_path + "/build/examples/openpose/openpose.bin",
        "--image_dir", os.path.dirname(image_path),
        "--write_json", output_folder,
        "--display", "0",
        "--render_pose", "0"
    ]
    
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print("Error running OpenPose:", e)
        return None

    # Find the generated JSON file
    json_files = [f for f in os.listdir(output_folder) if f.endswith(".json")]
    if not json_files:
        print("No JSON output found!")
        return None

    json_file_path = os.path.join(output_folder, json_files[0])

    # Read keypoints from JSON
    with open(json_file_path, "r") as f:
        data = json.load(f)

    # Extract keypoints
    if "people" in data and len(data["people"]) > 0:
        keypoints = data["people"][0]["pose_keypoints_2d"]
        return keypoints
    else:
        print("No keypoints detected!")
        return None

if __name__ == "__main__":
    image_path = "path/to/user_image.jpg"  # Replace with your image path
    keypoints = get_body_keypoints(image_path, openpose_path="/path/to/openpose")
    if keypoints:
        print("Extracted Keypoints:", keypoints)
    else:
        print("Failed to extract keypoints.")
