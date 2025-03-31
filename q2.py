import cv2
import numpy as np
import matplotlib.pyplot as plt

def erode_once(img, kernel):
    # Get dimensions
    k_h, k_w = kernel.shape
    pad_h, pad_w = k_h // 2, k_w // 2
    img_padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    eroded_img = np.zeros_like(img)
    
    # Erosion with fit and hit
    for i in range(pad_h, img_padded.shape[0] - pad_h):
        for j in range(pad_w, img_padded.shape[1] - pad_w):
            region = img_padded[i - pad_h:i + pad_h + 1, j - pad_w:j + pad_w + 1]
            eroded_img[i - pad_h, j - pad_w] = np.max(region * kernel)  # Fit condition using max value
    
    return eroded_img

def dilate_once(img, kernel):
    # Get dimensions
    k_h, k_w = kernel.shape
    pad_h, pad_w = k_h // 2, k_w // 2
    img_padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=255)
    dilated_img = np.zeros_like(img)
    
    # Dilation with fit and hit
    for i in range(pad_h, img_padded.shape[0] - pad_h):
        for j in range(pad_w, img_padded.shape[1] - pad_w):
            region = img_padded[i - pad_h:i + pad_h + 1, j - pad_w:j + pad_w + 1]
            dilated_img[i - pad_h, j - pad_w] = np.min(region * kernel)  # Hit condition using min value
    
    return dilated_img

def erode(img, kernel, iterations):
    for _ in range(iterations):
        img = erode_once(img, kernel)
    return img

def dilate(img, kernel, iterations):
    for _ in range(iterations):
        img = dilate_once(img, kernel)
    return img

def morphology_process(image_path, output_path):
    # Read the image
    img = cv2.imread(image_path, 0)
    if img is None:
        raise FileNotFoundError(f"Image at path {image_path} not found.")
    
    # Select appropriate structuring element
    kernel = np.ones((5, 5), np.uint8)
    
    # Apply erosion followed by dilation
    eroded = erode(img, kernel, iterations=2)
    dilated = dilate(eroded, kernel, iterations=2)
    
    # Save the result
    cv2.imwrite(output_path, dilated)
    
    # Display the original and processed images
    plt.figure(figsize=(12,6))
    plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Original'), plt.axis('off')
    plt.subplot(122), plt.imshow(dilated, cmap='gray'), plt.title('Processed'), plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    morphology_process('./resized_zzz.png', './output_2.png')
