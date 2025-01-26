# Image Upscaling Process: Detailed Step-by-Step Breakdown

## Image Upload and Initial Processing
1. **Image Selection**
   - User uploads image via Streamlit file uploader
   - Supported formats: JPG, PNG, BMP, TIFF
   - Image converted to NumPy array
   - Decoded using OpenCV

## Upscaling Preparation
2. **Image Preprocessing**
   - Determine original image dimensions
   - Calculate new dimensions based on scale factor
   - Ensure color space compatibility (BGR to RGB)

## Primary Enhancement Stages
3. **Lanczos Interpolation**
   - Resize image using Lanczos algorithm
   - Increase image size (2x, 3x, or 4x)
   - Mathematical reconstruction of pixel values
   - Minimize aliasing and preserve details

[DecompressionBombWarning: Image size (109499904 pixels) exceeds limit of 89478485 pixels, could be decompression bomb DOS attack.]

4. **Contrast Enhancement (CLAHE)**
   - Convert image to LAB color space
   - Split channels (Lightness, A, B)
   - Apply Contrast Limited Adaptive Histogram Equalization
   - Focus on lightness channel
   - Redistribute pixel intensities locally

5. **Sharpening (Unsharp Masking)**
   - Create Gaussian blur of original image
   - Subtract blurred image from original
   - Enhance edge details and textures
   - Adjust sharpness strength

## Final Processing
6. **Image Finalization**
   - Merge enhanced channels
   - Convert back to BGR color space
   - Clip pixel values to valid range (0-255)
   - Convert to 8-bit unsigned integer format

## User Interface Presentation
7. **Streamlit Display**
   - Show original image side-by-side with enhanced image
   - Display image dimensions
   - Provide download button for enhanced image

## Performance Considerations
8. **Optimization Techniques**
   - Use vectorized NumPy operations
   - Leverage OpenCV's optimized functions
   - Minimize memory allocation
   - Quick processing for real-time enhancement

## Error Handling
9. **Potential Failure Points**
   - Validate image upload
   - Handle unsupported image formats
   - Manage memory for large images
   - Provide user-friendly error messages
