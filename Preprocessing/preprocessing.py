import os
import torch
import cv2
import numpy as np
from torchvision import transforms
from PIL import Image
from model.u2net import U2NET  # Import U-2-Net model

# Load U-2-Net model
def load_u2net(model_path = r"C:\Users\mufeez kaiyoom\Desktop\Foss hack\U-2-Net-master\U-2-Net-master\U2NET\u2net.pth"):
    net = U2NET(3, 1)  # 3 input channels (RGB), 1 output channel (grayscale)
    net.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    net.eval()  # Set to evaluation mode
    return net

# Preprocess input image
def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((320, 320)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(image).unsqueeze(0)  # Add batch dimension

# Run U-2-Net and get segmentation mask
def get_segmentation_mask(model, image_tensor, original_size):
    with torch.no_grad():
        output = model(image_tensor)[0]  # Get first output from U-2-Net
        mask = output.squeeze().cpu().numpy()  # Convert to numpy array
        mask = (mask - mask.min()) / (mask.max() - mask.min())  # Normalize (0-1)
        mask = (mask * 255).astype(np.uint8)  # Convert to 0-255 scale

    # Resize mask to original image size
    mask = cv2.resize(mask, original_size, interpolation=cv2.INTER_LINEAR)
    
    # Convert to binary mask (thresholding)
    _, binary_mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)
    
    # Save mask
    cv2.imwrite("mask.png", binary_mask)
    return "mask.png"

# Extract garment using the mask
def extract_garment(image_path, mask_path):
    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

    # Ensure mask is binary
    _, binary_mask = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY)

    # Extract garment
    garment = cv2.bitwise_and(image, image, mask=binary_mask)

    # Convert to RGBA (for transparency)
    b, g, r = cv2.split(garment)
    alpha = binary_mask
    garment_rgba = cv2.merge([b, g, r, alpha])

    # Save final garment image
    output_path = "extracted_garment.png"
    cv2.imwrite(output_path, garment_rgba)
    return output_path

# Main function to process the image
def remove_bg(image_path):
    model = load_u2net()  # Load U-2-Net model
    image_tensor = preprocess_image(image_path)  # Preprocess image
    original_size = Image.open(image_path).size  # Get original size

    mask_path = get_segmentation_mask(model, image_tensor, original_size)  # Generate mask
    garment_path = extract_garment(image_path, mask_path)  # Extract garment
    
    print(f"Garment extracted and saved at: {garment_path}")

# Run the pipeline
if __name__ == "__main__":
    input_image = r"C:\Users\mufeez kaiyoom\Downloads\image.png"  # Change this to your image path
    remove_bg(input_image)
