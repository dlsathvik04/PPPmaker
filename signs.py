import cv2
import numpy as np
import os

def crop_handwritten_text(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"No contours found in {image_path}")
        return image

    # Combine all contours to form a single bounding box
    combined_contour = np.vstack(contours)
    x, y, w, h = cv2.boundingRect(combined_contour)

    # Crop the image to the bounding box
    cropped_image = image[y:y+h, x:x+w]

    # Save the cropped image
    cv2.imwrite(output_path, cropped_image)
    print(f"Cropped handwritten text saved to {output_path}")

def crop_handwritten_text_return(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a binary threshold to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print(f"No contours found in {image_path}")
        return image

    # Combine all contours to form a single bounding box
    combined_contour = np.vstack(contours)
    x, y, w, h = cv2.boundingRect(combined_contour)

    # Crop the image to the bounding box
    cropped_image = image[y:y+h, x:x+w]

    return cropped_image

def crop_signatures_in_folder(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"cropped_{filename}")
            crop_handwritten_text(input_path, output_path)


# # Example usage:
# input_folder = "./signs"
# output_folder = "./output"
# crop_signatures_in_folder(input_folder, output_folder)
