import cv2
import numpy as np
import matplotlib.pyplot as plt

def adaptive_butterworth_hpf(img, energy_ratio=0.7, order=3):
    """
    Fixed adaptive Butterworth High-pass Filter
    :param img: Input grayscale image (np.uint8)
    :param energy_ratio: Ratio of energy to retain in low-frequency (0-1)
    :param order: Filter order
    :return: Filtered image (np.uint8)
    """
    # 1. Fourier Transform
    dft = np.fft.fft2(img)
    dft_shift = np.fft.fftshift(dft)
    
    # 2. Calculate magnitude spectrum
    magnitude = np.abs(dft_shift)
    total_energy = np.sum(magnitude**2)
    
    # 3. Find cutoff frequency (D0)
    sorted_mag = np.sort(magnitude.flatten())[::-1]  # Descending order
    cumulative_energy = np.cumsum(sorted_mag**2)
    cutoff_idx = np.argmax(cumulative_energy > energy_ratio * total_energy)
    
    # Handle all-zero case
    if cutoff_idx == 0:
        cutoff_idx = 1  # Minimum 1 pixel radius
    
    # 4. Generate distance matrix
    rows, cols = img.shape
    crow, ccol = rows//2, cols//2
    y, x = np.ogrid[-crow:rows-crow, -ccol:cols-ccol]
    D = np.sqrt(x**2 + y**2)
    
    # Get D0 from sorted distances
    D_sorted = np.sort(D.flatten())
    D0 = D_sorted[cutoff_idx] if cutoff_idx < len(D_sorted) else D_sorted[-1]
    
    # Avoid D0=0
    D0 = max(D0, 1e-6)
    
    # 5. Butterworth filter (fixed normalization)
    mask = 1 / (1 + (D0 / (D + 1e-6)) ** (2*order))
    mask = np.nan_to_num(mask, nan=0.0, posinf=0.0, neginf=0.0)  # Handle NaN/INF
    
    # 6. Apply filter
    fshift = dft_shift * mask
    
    # 7. Inverse FFT with safe normalization
    img_back = np.abs(np.fft.ifft2(np.fft.ifftshift(fshift)))
    
    # Safe normalization
    if np.max(img_back) - np.min(img_back) < 1e-6:
        return np.zeros_like(img, dtype=np.uint8)
    else:
        img_normalized = 255 * (img_back - np.min(img_back)) / (np.max(img_back) - np.min(img_back))
        return np.uint8(np.clip(img_normalized, 0, 255))

if __name__ == "__main__":
    # Read image
    img = cv2.imread('sudoku.png', 0)
    if img is None:
        raise FileNotFoundError("Image not found!")
    
    # Process
    enhanced = adaptive_butterworth_hpf(img)
    
    # Save the result
    cv2.imwrite('output_1.png', enhanced)
    
    # Display
    plt.figure(figsize=(12,6))
    plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Original'), plt.axis('off')
    plt.subplot(122), plt.imshow(enhanced, cmap='gray'), plt.title('Enhanced'), plt.axis('off')
    plt.tight_layout()
    plt.show()