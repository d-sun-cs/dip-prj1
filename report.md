# Project Report

## 1. Project Content

This project focuses on two main tasks in digital image processing: **Image Enhancement** and **Morphology**. The first task involves sharpening an image to highlight its edges and details using an image enhancement algorithm. The second task requires designing a morphological algorithm to remove noise from an image. Both tasks must be implemented without directly using third-party libraries for the key image processing steps.

## 2. Method Description

### 2.1 Image Enhancement
For image enhancement, we implemented a combination of Gaussian blur and adaptive thresholding:

1. **Gaussian Blur**: 
   - Gaussian blur is a technique used to smooth an image by reducing noise and detail. It works by replacing each pixel's value with a weighted average of its neighbors, where the weights are determined by a Gaussian distribution. This ensures that closer pixels have a higher influence on the result, creating a natural smoothing effect.
   - In our implementation, we generated a Gaussian kernel based on the specified kernel size and standard deviation. The kernel was then applied to the image using convolution, where each pixel was updated based on the weighted sum of its surrounding pixels.

2. **Adaptive Thresholding**:
   - After smoothing the image, we applied adaptive thresholding. This method calculates a threshold for each pixel based on the mean intensity of its local neighborhood, subtracting a constant \(C\). Pixels with intensity values above the threshold are set to one value (e.g., white), while others are set to another value (e.g., black). This approach enhances edges and details by dynamically adjusting to local image characteristics.

### 2.2 Morphology
For noise removal, we implemented a morphological opening operation, which consists of two steps:

1. **Erosion**:
   - The image is eroded using a structuring element, which removes small noise by shrinking the regions and eliminating isolated pixels.

2. **Dilation**:
   - After erosion, the image is dilated using the same structuring element. This step restores the size and shape of the main structures in the image.

The overall operation, known as **opening**, is effective for removing small noise while preserving the primary structures of the image.

## 3. Experiment Results and Analysis

### 3.1 Results
- **Image Enhancement**:
  - The enhanced image (output_1.png) shows significantly improved edge sharpness and detail visibility. The Gaussian blur effectively reduces noise, while adaptive thresholding highlights the edges by dynamically adjusting the threshold.
- **Morphology**:
  - The noise-removed image (output_2.png) demonstrates effective suppression of small noise while preserving the main content. The morphological opening operation successfully removes isolated noise points and smooths the image.

### 3.2 Advantages and Disadvantages

#### Image Enhancement
- **Advantages**:
  - Gaussian blur reduces noise while preserving important features.
  - Adaptive thresholding dynamically adjusts to local image characteristics, enhancing edges effectively.
- **Disadvantages**:
  - Some small noise points remain visible in the enhanced image. This is likely because the Gaussian blur does not completely eliminate high-frequency noise, and the adaptive thresholding may misclassify some noisy pixels as edges.

#### Morphology
- **Advantages**:
  - The opening operation is robust in removing small noise while maintaining the integrity of larger objects.
  - The algorithm is flexible and can be adjusted by changing the structuring element size and the number of iterations.
- **Disadvantages**:
  - The processed image may retain small edge artifacts or "spikes" along the boundaries of objects.
  - If the number of erosion and dilation iterations is not carefully controlled, the algorithm can distort the image structure, either over-smoothing or over-shrinking the objects.

## 4. Summary

### Difficulties
- Implementing the algorithms without using third-party libraries for key processing steps required a deeper understanding of the underlying mathematical operations.
- Fine-tuning parameters such as kernel size, standard deviation, and structuring element dimensions to achieve optimal results was challenging.

### Knowledge Learned
- Learned the practical implementation of Gaussian blur, which was not covered in detail during the lectures. This project provided an opportunity to explore and understand its application in image processing.
- Gained hands-on experience with adaptive thresholding and morphological operations.
- Understood the importance of parameter selection and its impact on algorithm performance.
- Learned the trade-offs between algorithm complexity and performance in real-world applications.

In conclusion, this project provided valuable insights into image processing techniques and their implementation from scratch. It also highlighted the challenges of balancing algorithm efficiency and accuracy.
