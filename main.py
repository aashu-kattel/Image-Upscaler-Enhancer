import cv2
import numpy as np
import streamlit as st
from PIL import Image
import io

class AdvancedImageUpscaler:
    @staticmethod
    def unsharp_mask(image, sigma=1.0, strength=1.5):
        """
        Apply unsharp masking to enhance image details
        
        Args:
            image (numpy.ndarray): Input image
            sigma (float): Gaussian blur sigma
            strength (float): Sharpening strength
        
        Returns:
            numpy.ndarray: Sharpened image
        """
        # Gaussian blur
        blurred = cv2.GaussianBlur(image, (0, 0), sigma)
        
        # Calculate unsharp mask
        sharpened = cv2.addWeighted(image, 1 + strength, blurred, -strength, 0)
        
        return sharpened

    @staticmethod
    def enhance_contrast(image):
        """
        Enhance image contrast using CLAHE (Contrast Limited Adaptive Histogram Equalization)
        
        Args:
            image (numpy.ndarray): Input image
        
        Returns:
            numpy.ndarray: Contrast-enhanced image
        """
        # Convert to LAB color space
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        
        # Split the LAB image to different channels
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L-channel
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        
        # Merge the CLAHE enhanced L-channel with the a and b channel
        limg = cv2.merge((cl,a,b))
        
        # Convert image from LAB to BGR color space
        enhanced = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        
        return enhanced

    @staticmethod
    def adjust_saturation(image, saturation_scale=3.0):
        """
        Adjust the saturation of the image
        
        Args:
            image (numpy.ndarray): Input image
            saturation_scale (float): Scale to adjust saturation by
        
        Returns:
            numpy.ndarray: Saturation-adjusted image
        """
        # Convert image to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        
        # Scale the saturation channel
        hsv[:, :, 1] = cv2.multiply(hsv[:, :, 1], saturation_scale)
        
        # Convert back to BGR color space
        saturated_image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        
        return saturated_image

    def upscale(self, image, scale_factor=2):
        """
        Advanced upscaling with multiple enhancement techniques
        
        Args:
            image (numpy.ndarray): Input image
            scale_factor (int): Scale factor for upscaling
        
        Returns:
            numpy.ndarray: Enhanced and upscaled image
        """
        # Upscale using Lanczos
        upscaled = cv2.resize(
            image, 
            (image.shape[1] * scale_factor, image.shape[0] * scale_factor), 
            interpolation=cv2.INTER_LANCZOS4
        )
        
        # Enhance contrast
        contrast_enhanced = self.enhance_contrast(upscaled)
        
        # Apply unsharp masking for detail enhancement
        sharpened = self.unsharp_mask(contrast_enhanced, sigma=1.0, strength=1.5)
        
        return sharpened

def main():
    # Streamlit page configuration
    st.set_page_config(
        page_title="Img Upscale/Enhancer", 
        page_icon=":camera:",
        layout="wide"
    )

    # Title and description
    st.title("🚀 Image Upscaler/Enhancer")
    st.write("Dramatically improve image quality with multi-stage enhancement")

    # Sidebar for user inputs
    st.sidebar.header("Enhancement Options")
    
    # Scale factor selection
    scale_factor = st.sidebar.selectbox(
        "Select Upscaling Factor", 
        [2, 3, 4],
        index=0
    )

    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image", 
        type=["jpg", "jpeg", "png", "bmp", "tiff"]
    )

    # Main content processing
    if uploaded_file is not None:
        # Read the image
        file_bytes = np.array(bytearray(uploaded_file.read()), dtype=np.uint8)
        original_image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # Create columns for before and after with different widths
        col1, spacer, col2 = st.columns([4, 0.5, 5])

        with col1:
            st.subheader("Original Image")
            # Display original image at 90% of column width
            st.image(
                cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB),
                use_column_width=True,
                width=300  # Base width for original image
            )
            
            # Display original image details
            orig_height, orig_width = original_image.shape[:2]
            st.write(f"Original Size: {orig_width}x{orig_height}")

        with col2:
            st.subheader("Enhanced Image")
            
            # Perform upscaling and enhancement
            upscaler = AdvancedImageUpscaler()
            enhanced_image = upscaler.upscale(original_image, scale_factor)
            
            # Display enhanced image at full column width
            st.image(
                cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB),
                use_column_width=True,
                width=400  # Larger base width for enhanced image
            )
            
            # Display enhanced image details
            new_height, new_width = enhanced_image.shape[:2]
            st.write(f"Enhanced Size: {new_width}x{new_height}")

            # Download button for enhanced image
            enhanced_pil = Image.fromarray(cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2RGB))
            buf = io.BytesIO()
            enhanced_pil.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Download Enhanced Image",
                data=byte_im,
                file_name=f"enhanced_{uploaded_file.name}",
                mime="image/png"
            )

    else:
        # Placeholder instructions
        st.warning("Please upload an image to begin enhancement.")
        st.info("Supported formats: JPG, PNG, BMP, TIFF")

    # Additional information
    st.sidebar.markdown("---")
    st.sidebar.info(
        "Enhancement techniques:\n"
        "1. Lanczos Upscaling\n"
        "2. Adaptive Contrast Enhancement\n"
        "3. Unsharp Masking for Detail Preservation"
    )

# Run the app
if __name__ == "__main__":
    main()