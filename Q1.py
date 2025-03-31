import cv2
import numpy as np
import matplotlib.pyplot as plt

def gaussian_blur(img, kernel_size=3, sigma=0):
    """
    Apply Gaussian blur to the input image.
    :param img: Input grayscale image (np.uint8)
    :param kernel_size: Size of the Gaussian kernel (must be odd)
    :param sigma: Standard deviation for Gaussian kernel
    :return: Blurred image (np.uint8)
    """
    # Generate Gaussian kernel
    k = kernel_size // 2
    x = np.arange(-k, k + 1)
    y = np.arange(-k, k + 1)
    x, y = np.meshgrid(x, y)
    if sigma <= 0:
        sigma = 0.3 * ((kernel_size - 1) * 0.5 - 1) + 0.8
    gaussian_kernel = np.exp(-(x**2 + y**2) / (2 * sigma**2)) / (2 * np.pi * sigma**2)
    gaussian_kernel /= gaussian_kernel.sum()
    
    # Apply convolution
    pad_size = kernel_size // 2
    img_padded = np.pad(img, pad_size, mode='constant', constant_values=0)
    blurred_img = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = img_padded[i:i + kernel_size, j:j + kernel_size]
            blurred_img[i, j] = np.sum(region * gaussian_kernel)
    
    return blurred_img

def adaptive_thresholding(img, block_size=7, C=2):
    """
    Apply adaptive thresholding to the input image.
    :param img: Input grayscale image (np.uint8)
    :param block_size: Size of the local region (must be odd)
    :param C: Constant subtracted from the mean
    :return: Thresholded image (np.uint8)
    """
    # Ensure block size is odd
    if block_size % 2 == 0:
        raise ValueError("Block size must be odd.")
    
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
            region = img_padded[i:i + block_size, j:j + block_size]
            local_mean = np.mean(region)
            if img[i, j] > local_mean - C:
                thresholded_img[i, j] = 0
            else:
                thresholded_img[i, j] = 255
    
    return thresholded_img

if __name__ == "__main__":
    # Read image
    img = cv2.imread('sudoku.png', 0)
    if img is None:
        raise FileNotFoundError("Image not found!")
    
    # Apply Gaussian blur
    blurred_img = gaussian_blur(img)
    
    # Apply adaptive thresholding
    enhanced_img = adaptive_thresholding(blurred_img)
    
    # Save the result
    cv2.imwrite('output_1.png', enhanced_img)
    
    # Display
    plt.figure(figsize=(12,6))
    plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Original'), plt.axis('off')
    plt.subplot(132), plt.imshow(blurred_img, cmap='gray'), plt.title('Gaussian Blurred'), plt.axis('off')
    plt.subplot(133), plt.imshow(enhanced_img, cmap='gray'), plt.title('Enhanced'), plt.axis('off')
    plt.tight_layout()
    plt.show()