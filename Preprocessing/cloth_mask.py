import os
from rembg import remove
from PIL import Image

def remove_background(input_path, output_dir_transparent, output_dir_mask):
    """
    Removes the background from a clothing image.
    Saves the transparent image (with background removed) in output_dir_transparent,
    and the binary mask (extracted from the alpha channel) in output_dir_mask.
    Both files use the same base name (in PNG format).
    """
    # Create output directories if they don't exist.
    os.makedirs(output_dir_transparent, exist_ok=True)
    os.makedirs(output_dir_mask, exist_ok=True)

    # Extract base file name (without extension).
    directory, filename = os.path.split(input_path)
    base, _ = os.path.splitext(filename)

    # Define output file paths.
    output_no_bg = os.path.join(output_dir_transparent, base + ".png")
    output_mask = os.path.join(output_dir_mask, base + ".png")

    # Open the input image and ensure it has an alpha channel.
    input_image = Image.open(input_path).convert("RGBA")

    # Remove background using rembg.
    output_image = remove(input_image)
    output_image.save(output_no_bg)
    print(f"Saved background-removed image as: {output_no_bg}")

    # Extract the mask (alpha channel) and save.
    mask = output_image.getchannel("A")
    mask.save(output_mask)
    print(f"Saved mask image as: {output_mask}")

if __name__ == "__main__":
    # Path to your input cloth image.
    input_cloth = r"B:\fosshack\foss\Meta-Closet\models\datasets\test\cloth\01260_00.jpg"  

    # Directories to save the output images.
    output_dir_transparent = r"A:\output_transparent"
    output_dir_mask = r"A:\output_mask"

    remove_background(input_cloth, output_dir_transparent, output_dir_mask)
