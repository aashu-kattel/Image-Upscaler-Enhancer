Ref: https://claude.ai/chat/b2bba9ac-41cc-4154-8fef-c2af55ac70d3

##Image Scaler/Enhancer leveraging Lanczos Interpolation and CLAHE Algorithm

To Run: streamlit run main.py

[

1. Lanczos Interpolation for initial upscaling
2. CLAHE (Contrast Limited Adaptive Histogram Equalization)
- Enhances local contrast
- Preserves edge details

3. Unsharp Masking
- Sharpens image details
- Makes edges and textures more pronounced

]

The key OOP elements are:
-AdvancedImageUpscaler class
-Encapsulation of methods like unsharp_mask(), enhance_contrast(), and upscale()
-Static methods for specific image processing techniques
-Class-based approach to image enhancement

The main class AdvancedImageUpscaler contains methods that:
1. Process images
2. Perform specific transformations
3. Provide a structured approach to image upscaling