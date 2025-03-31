import cv2
import numpy as np
import matplotlib.pyplot as plt
def plot_comparison(original, filtered, title_filtered):
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 5), sharex=True, sharey=True)
    ax1.imshow(original, cmap='gray')
    ax1.set_title('Original')
    ax1.axis('off')
    ax2.imshow(filtered, cmap='gray')
    ax2.set_title(title_filtered)
    ax2.axis('off')
    plt.show()

def gaussian_blur(img, kernel_size, sigma):
    # Generate Gaussian kernel
    k = kernel_size // 2
    x, y = np.meshgrid(np.arange(-k, k+1), np.arange(-k, k+1))
    if sigma <= 0:
        sigma = 0.3 * ((kernel_size-1)*0.5-1)+0.8
    gaussian_kernel = 1 / (2 * np.pi * sigma**2) * np.exp(-(x**2 + y**2) / (2 * sigma**2))
    gaussian_kernel /= gaussian_kernel.sum()

    # Apply convolution
    pad = kernel_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad)), mode='constant', constant_values=0)
    blurred = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+kernel_size, j:j+kernel_size]
            blurred[i, j] = np.sum(region * gaussian_kernel)
    return blurred

def adaptive_threshold(img, block_size, C):
    # Ensure block size is odd
    if block_size % 2 == 0:
        raise ValueError("Block size must be odd.")
    
    pad = block_size // 2
    padded = np.pad(img, ((pad, pad), (pad, pad)), mode='constant', constant_values=255)
    thresholded = np.zeros_like(img)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            region = padded[i:i+block_size, j:j+block_size]
            local_mean = np.mean(region)
            thresholded[i, j] = 0 if img[i, j] > local_mean - C else 255
    return thresholded

# Read image
image = cv2.imread('sudoku.png', cv2.IMREAD_GRAYSCALE)

gray = gaussian_blur(image, 3, 0)
thresh = adaptive_threshold(gray, 7, 2)

# Plot result
plot_comparison(gray, thresh, 'Processed')

# Save result
cv2.imwrite('output_1.png', thresh)
