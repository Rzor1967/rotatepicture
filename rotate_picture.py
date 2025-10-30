from PIL import Image, ImageFilter
import numpy as np

def open_image(file_path):
    """Open an image file and return a PIL Image object."""
    img = Image.open(file_path).convert('L') # Convert to grayscale
    filtered_img = img.filter(ImageFilter.MedianFilter(size=3))
    bitmap = np.array(filtered_img)

    binary = (bitmap > 128).astype(int) # Binarize the image
    return binary

def find_bounding_box(binary_image):
    """Find the bounding box of the white area in a binary image."""
    rows = np.any(binary_image, axis=1)
    cols = np.any(binary_image, axis=0)
    y_min, y_max = np.where(rows)[0][[0, -1]]
    x_min, x_max = np.where(cols)[0][[0, -1]]
    return (x_min, y_min, x_max, y_max)

if __name__ == "__main__":
    image_path = "14.jpg"
    import sys
    if len(sys.argv) != 2:
        print("Usage: python rotate_picture.py <image_path>")
        sys.exit(1)

    image_path = sys.argv[1]
    binary_image = open_image(image_path)
    (height, width) = binary_image.shape
    print(f"Image dimensions: {width}x{height}")
    bbox = find_bounding_box(binary_image)
    print(f"Bounding box: {bbox}")