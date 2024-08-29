import cv2

def save_image_with_size_limit(image_array, file_path, size_threshold_kb, max_attempts=100):
    """
    Save an image to a file with a size under a specified threshold.

    Parameters:
    - image_array: The image as a numpy array.
    - file_path: The path where the image will be saved.
    - size_threshold_kb: The maximum file size in kilobytes.
    - max_attempts: The maximum number of attempts to reduce size.
    """
    # Start with the best quality (for JPEG)
    quality = 95
    success = False

    for attempt in range(max_attempts):
        # Encode the image to a memory buffer with the current quality setting
        is_success, buffer = cv2.imencode('.jpg', image_array, [cv2.IMWRITE_JPEG_QUALITY, quality])

        # Check the size of the buffer
        file_size_kb = len(buffer) / 1024
        print(file_size_kb)

        if file_size_kb <= size_threshold_kb:
            # If the size is under the threshold, save the file
            with open(file_path, 'wb') as f:
                f.write(buffer)
            success = True
            break

        # If the file size is too large, reduce the quality
        quality -= 10

        # if quality < 10:  # Prevent quality from going too low
        #     break

    if not success:
        raise ValueError(f"Could not reduce image size under {size_threshold_kb} KB after {max_attempts} attempts.")