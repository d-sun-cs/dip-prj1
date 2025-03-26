import cv2
import numpy as np
import matplotlib.pyplot as plt

def adaptive_thresholding(img, block_size=11, C=2):
    """
    Apply adaptive thresholding to the input image.
    :param img: Input grayscale image (np.uint8)
    :param block_size: Size of the local region (must be odd)
    :param C: Constant subtracted from the mean
    :return: Thresholded image (np.uint8)
    """
    # Get image dimensions
    rows, cols = img.shape
    
    # Pad the image
    pad_size = block_size // 2
    img_padded = np.pad(img, pad_size, mode='constant', constant_values=255)
    
    # Initialize the output image
    thresholded_img = np.zeros_like(img)
    
    # Apply adaptive thresholding
    for i in range(rows):
        for j in range(cols):
            region = img_padded[i:i + block_size, j:j + block_size]  # Corrected indexing
            local_mean = np.mean(region)
            threshold = local_mean - C
            thresholded_img[i, j] = 0 if img[i, j] > threshold else 255  # Inverted output
    
    return thresholded_img

if __name__ == "__main__":
    # Read image
    img = cv2.imread('sudoku.png', 0)
    if img is None:
        raise FileNotFoundError("Image not found!")
    
    # Process
    enhanced = adaptive_thresholding(img)
    
    # Save the result
    cv2.imwrite('output_1.png', enhanced)
    
    # Display
    plt.figure(figsize=(12,6))
    plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Original'), plt.axis('off')
    plt.subplot(122), plt.imshow(enhanced, cmap='gray'), plt.title('Enhanced'), plt.axis('off')
    plt.tight_layout()
    plt.show()