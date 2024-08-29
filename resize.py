from PIL import Image
import io
import os

import cv2

from compressor import save_image_with_size_limit

output_dir = "./output_resize"
input_dir = './input_resize'
photo_suffix = 'photo.jpg'
size_threshold = 30

def resize_image_to_target_kb(image_path, target_kb, quality=95):
    """Resizes an image to approximately the target size in KB."""

    img = Image.open(image_path)

    # Initial resize to get closer to the target size
    img.thumbnail((img.width // 2, img.height // 2))

    while True:
        # Save the image to a buffer to get its size
        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality)
        size_kb = buffer.getbuffer().nbytes / 1024

        # Check if the size is within the desired range
        if size_kb <= target_kb:
            break

        # Resize the image further
        new_width = int(img.width * 0.9)
        new_height = int(img.height * 0.9)
        img = img.resize((new_width, new_height))
    return img

os.makedirs(output_dir, exist_ok=True)

i =0
for photo in os.listdir(input_dir):
    i+=1
    # img = cv2.imread(os.path.join(input_dir, photo))
    # save_image_with_size_limit(img, os.path.join(output_dir, photo),size_threshold)
    res = resize_image_to_target_kb(os.path.join(input_dir, photo), size_threshold)
    res.save(os.path.join(output_dir, photo))
