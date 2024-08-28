import cv2
import numpy as np

def resize_and_stack_images(img1, img2):
    # Get the dimensions of the first image
    height1, width1 = img1.shape[:2]

    # Calculate the desired height for the second image
    desired_height2 = height1 // 6

    # Calculate the new width for the second image to maintain its aspect ratio
    aspect_ratio2 = img2.shape[1] / img2.shape[0]
    new_height2 = desired_height2
    new_width2 = int(new_height2 * aspect_ratio2)

    # Resize the second image to the calculated dimensions
    img2_resized = cv2.resize(img2, (new_width2, new_height2))

    # Calculate the padding needed to match the width of the first image
    if new_width2 < width1:
        padding_needed = width1 - new_width2
        padding_left = padding_needed // 2
        padding_right = padding_needed - padding_left
        # Add padding to the left and right sides
        img2_resized = cv2.copyMakeBorder(img2_resized, 0, 0, padding_left, padding_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])

    # Stack the two images vertically
    stacked_image = np.vstack((img1, img2_resized))

    return stacked_image

# # Load the images
# img1 = cv2.imread('output/passport_IMG_20230211_181757.jpg')
# img2 = cv2.imread('output/cropped_signature.jpg')

# # Stack the images
# result = resize_and_stack_images(img1, img2)

# # Save or display the result
# cv2.imwrite('stacked_image.jpg', result)