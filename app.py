import os

import cv2

from compressor import save_image_with_size_limit
from cropper import detect_and_crop_face_return
from merger import resize_and_stack_images
from signs import crop_handwritten_text_return

output_dir = "./output"
input_dir = './input'
photo_suffix = 'photo.jpg'
size_threshold = 70


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
        si = crop_handwritten_text_return(sign)
        res = resize_and_stack_images(pp, si)
        # cv2.imwrite(os.path.join(output_dir, person_dir) + ".jpg", res)
        save_image_with_size_limit(res, os.path.join(output_dir, person_dir) + ".jpg", size_threshold )
        print("successfully processed ", person_dir)
