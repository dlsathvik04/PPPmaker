import os

import cv2
import numpy as np

from compressor import save_image_with_size_limit
from cropper import detect_and_crop_face_return
from merger import resize_and_stack_images
from signs import crop_handwritten_text_return

output_dir = "./output"
input_dir = './input'
photo_suffix = 'photo.jpg'
size_threshold = 30

def increase_contrast_and_denoise(image: np.ndarray) -> np.ndarray:
    # Step 1: Convert the image to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    
    # Step 2: Split the LAB image into L, A, and B channels
    l, a, b = cv2.split(lab)
    
    # Step 3: Apply histogram equalization to the L channel
    l = cv2.equalizeHist(l)
    
    # Step 4: Merge the channels back together
    lab = cv2.merge((l, a, b))
    
    # Step 5: Convert back to BGR color space
    contrast_image = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Step 6: Apply Gaussian blur to reduce noise
    # Adjust the kernel size as needed (must be positive and odd)
    denoised_image = cv2.GaussianBlur(contrast_image, (7, 7), 0)
    
    # Alternatively, you can use median blur for stronger noise reduction:
    # denoised_image = cv2.medianBlur(contrast_image, 5)
    
    # Step 7: Further enhance contrast and brightness if needed
    alpha = 2.5  # Contrast control (1.0-3.0)
    beta = 75   # Brightness control (0-100)
    
    final_image = cv2.convertScaleAbs(denoised_image, alpha=alpha, beta=beta)
    
    return final_image



os.makedirs(output_dir, exist_ok=True)
i = 0
for person_dir in os.listdir(input_dir):
    i+=1
    if os.path.isdir(os.path.join(input_dir,person_dir)):
        person_files = os.listdir(os.path.join(input_dir,person_dir))
        if (len(person_files) != 2):
            print("the directory ", person_dir, " is not correctly structured")
            exit(0)
        photo = None
        sign = None
        for f in person_files:
            if f.endswith("photo.jpg"):
                photo = os.path.join(input_dir, person_dir, f)
            else :
                sign = os.path.join(input_dir, person_dir, f)
        if (photo is None) or (sign is None):
            print("the directory ", person_dir, " is not correctly structured")
            exit(0)
        pp = detect_and_crop_face_return(photo)
        si = increase_contrast_and_denoise(crop_handwritten_text_return(sign))
        res = resize_and_stack_images(pp, si)
        # cv2.imwrite(os.path.join(output_dir, person_dir) + ".jpg", res)
        save_image_with_size_limit(res, os.path.join(output_dir, person_dir) + ".jpg", size_threshold )
        print("successfully processed ", person_dir)
