# File organization logic
import os

class FileOrganizer:
    def __init__(self, base_output_dir="output_documents"):
        self.base_output_dir = base_output_dir
        if not os.path.exists(self.base_output_dir):
            os.makedirs(self.base_output_dir)

    def store_document(self, image_path, category_path, document_name, metadata):
        # Placeholder for storing document
        # category_path would be like 'health/prescriptions'
        # document_name would be like '2025-04-03_invoice_car_tires_001.jpg'
        target_folder = os.path.join(self.base_output_dir, category_path)
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        
        target_file_path = os.path.join(target_folder, document_name)
        # For now, just print. Later, this will copy/move the file and write metadata.
        print(f"Storing {image_path} to {target_file_path}")
        print(f"With metadata: {metadata}")
        # shutil.copy(image_path, target_file_path)
        # Add metadata writing using PyExifTool here
        return target_file_path
