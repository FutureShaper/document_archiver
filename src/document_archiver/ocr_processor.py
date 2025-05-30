# OCR processing logic using Docling
from docling.document_converter import DocumentConverter
from typing import Optional, Union # For Python 3.9 compatibility

class OCRProcessor:
    def __init__(self):
        # Initialize Docling DocumentConverter
        self.converter = DocumentConverter()

    def process_image(self, image_path: str) -> Optional[str]: # Changed to Optional[str]
        """
        Processes an image file using Docling to extract text.

        Args:
            image_path: The path to the image file.

        Returns:
            The extracted text as a string, or None if processing fails.
        """
        print(f"Processing image: {image_path} with Docling OCR")
        try:
            # Docling's convert method should auto-detect file types based on extension or content.
            # For specific image handling, if needed, one might explore Docling's options further,
            # but typically direct path to an image file is sufficient.
            result = self.converter.convert(source=image_path)
            
            if result and result.document:
                # Export to plain text for LLM processing
                extracted_text = result.document.export_to_text()
                # You can also use result.document.export_to_markdown() if markdown is preferred
                # extracted_text = result.document.export_to_markdown()
                return extracted_text
            else:
                print(f"Docling could not process the document: {image_path}")
                return None
        except Exception as e:
            print(f"Error during OCR processing for {image_path}: {e}")
            return None

# Example usage (for testing purposes)
if __name__ == '__main__':
    # This is a placeholder for a test image path.
    # It will attempt to create a dummy image file (dummy_test_image.png)
    # in the same directory as this script.
    
    import os
    # PIL is part of Pillow, which was installed as a dependency of docling or directly.
    # If this import fails, ensure Pillow is correctly installed in the 'document_archiver' env.
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("Pillow library (PIL) not found. Please ensure it's installed: pip install Pillow")
        exit()


    dummy_image_path = "dummy_test_image.png"
    text_to_draw = "This is a test document image for Docling OCR. Invoice #123 Date: 2024-01-15"

    if not os.path.exists(dummy_image_path):
        try:
            img = Image.new('RGB', (600, 150), color = (255, 255, 255))
            d = ImageDraw.Draw(img)
            
            try:
                # Try a common font, fall back to default if not available
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                try:
                    font = ImageFont.truetype("DejaVuSans.ttf", 20) # Common on Linux
                except IOError:
                    font = ImageFont.load_default() # Fallback
            
            d.text((10,10), text_to_draw, fill=(0,0,0), font=font)
            img.save(dummy_image_path)
            print(f"Created dummy image: {dummy_image_path}")
        except Exception as e:
            print(f"Could not create dummy image: {e}. Please create it manually for testing.")
            # If image creation fails, no point in continuing the test here.
            exit()


    if os.path.exists(dummy_image_path):
        processor = OCRProcessor()
        extracted_text = processor.process_image(dummy_image_path)
        if extracted_text:
            print("\nExtracted Text:\n---\n", extracted_text, "\n---")
        else:
            print("No text extracted or an error occurred during OCR processing.")
        # Consider leaving the dummy image for inspection or further tests
        # os.remove(dummy_image_path)
        # print(f"Cleaned up dummy image: {dummy_image_path}")
    else:
        print(f"Test image {dummy_image_path} was not created or found. Skipping example usage.")
