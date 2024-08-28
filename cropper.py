import cv2
import os

def crop_to_passport_size(image, face_rect):
    passport_aspect_ratio = 413 / 531  # Width to height ratio of a passport photo
    
    x, y, w, h = face_rect

    # Calculate the center of the face rectangle
    center_x, center_y = x + w // 2, y + h // 2

    # Double the width and height
    new_w = int(w * 2.5)
    new_h =int(h * 2.5
)
    # Adjust new width and height to maintain the passport aspect ratio
    if new_w / new_h > passport_aspect_ratio:
        new_w = int(new_h * passport_aspect_ratio)
    else:
        new_h = int(new_w / passport_aspect_ratio)

    # Calculate the new cropping coordinates
    x1 = max(0, center_x - new_w // 2)
    y1 = max(0, center_y - new_h // 2)
    x2 = min(image.shape[1], center_x + new_w // 2)
    y2 = min(image.shape[0], center_y + new_h // 2)

    # Crop the image with the new dimensions
    cropped_image = image[y1:y2, x1:x2]

    # Ensure the cropped region has the correct aspect ratio
    cropped_height, cropped_width = cropped_image.shape[:2]
    if cropped_width / cropped_height != passport_aspect_ratio:
        # Adjust the cropped region to maintain the aspect ratio
        if cropped_width / cropped_height > passport_aspect_ratio:
            # Width is too wide, adjust it
            new_width = int(cropped_height * passport_aspect_ratio)
            x1 = max(0, center_x - new_width // 2)
            x2 = min(image.shape[1], center_x + new_width // 2)
        else:
            # Height is too tall, adjust it
            new_height = int(cropped_width / passport_aspect_ratio)
            y1 = max(0, center_y - new_height // 2)
            y2 = min(image.shape[0], center_y + new_height // 2)

        cropped_image = image[y1:y2, x1:x2]

    # Resize to the passport photo size
    passport_image = cv2.resize(cropped_image, (413, 531))

    return passport_image

def detect_and_crop_face(image_path, output_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale (needed for face detection)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load the pre-trained Haar Cascade face detector from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) > 0:
        # Take the first detected face (assuming one face per image)
        face_rect = faces[0]
        
        # Crop and resize the image to passport size
        passport_image = crop_to_passport_size(image, face_rect)
        
        # Save the cropped image
        cv2.imwrite(output_path, passport_image)
        print(f"Saved cropped image to {output_path}")
    else:
        print(f"No face detected in {image_path}")

def detect_and_crop_face_return(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale (needed for face detection)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Load the pre-trained Haar Cascade face detector from OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    if len(faces) > 0:
        # Take the first detected face (assuming one face per image)
        face_rect = faces[0]
        
        # Crop and resize the image to passport size
        passport_image = crop_to_passport_size(image, face_rect)
        return passport_image
        
    else:
        print(f"No face detected in {image_path}")

def crop_images_in_folder(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Process each image in the folder
    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"passport_{filename}")
            detect_and_crop_face(input_path, output_path)




# # Example usage:
# input_folder = "./input"
# output_folder = "./output"
# crop_images_in_folder(input_folder, output_folder)
