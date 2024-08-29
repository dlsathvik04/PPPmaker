import cv2
import numpy as np

def resize_and_stack_images(img1, img2):
    # Get the dimensions of the first image
    height1, width1 = img1.shape[:2]

    # Calculate the desired height for the second image (1/6th of the first image's height)
    desired_height2 = height1 // 6

    # Calculate the new width for the second image while maintaining its aspect ratio
    aspect_ratio2 = img2.shape[1] / img2.shape[0]
    new_height2 = desired_height2
    new_width2 = int(new_height2 * aspect_ratio2)

    # Resize the second image
    img2_resized = cv2.resize(img2, (new_width2, new_height2))

    # If the resized width of the second image is less than the first image's width,
    # add padding to the left and right to match the width
    if new_width2 < width1:
        padding_needed = width1 - new_width2
        padding_left = padding_needed // 2
        padding_right = padding_needed - padding_left
        img2_resized = cv2.copyMakeBorder(img2_resized, 0, 0, padding_left, padding_right, cv2.BORDER_CONSTANT, value=[255, 255, 255])
    elif new_width2 > width1:
        # Alternatively, if the second image's width is greater, you can resize it down to the width of the first image
        img2_resized = cv2.resize(img2_resized, (width1, desired_height2))

    # Now both images have the same width, stack them vertically
    stacked_image = np.vstack((img1, img2_resized))

    return stacked_image
# Load the images
# img1 = cv2.imread('input/ANITESWARI/ANITESWARI_photo.jpg')
# img2 = cv2.imread('input/ANITESWARI/ANITESWARI.jpg')

# # Stack the images
# result = resize_and_stack_images(img1, img2)

# # Save or display the result
# cv2.imwrite('stacked_image.jpg', result)