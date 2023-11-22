import cv2
import os
import shutil
import glob
import logging

# Configure basic logging 
logging.basicConfig(
    filename="processing.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# CONSTANTS
EXTRA_SPACE = 50
MIN_WIDTH = 400
MIN_HEIGHT = 50

def process_tiff_file(input_file, output_dir):
    """
    Process a TIFF file, extract relevant regions, and save them as images.

    Args:
        input_file (str): The path to the input TIFF file.
        output_dir (str): The directory to save the extracted images.

    Returns:
        None
    """
    try:
        # Load the TIFF image
        tif_image = cv2.imread(input_file)

        # Check if image was loaded successfully
        if tif_image is None:
            logging.error(f"Could not read {input_file}. Skipping..")
            return
        
        # Extract relevant regions and save them as images
        file_name = os.path.basename(input_file)
        gray_image = cv2.cvtColor(tif_image, cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image, 200, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        output_counter = 0

        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[1])
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w >= MIN_WIDTH and h > MIN_HEIGHT:
                new_x = x
                new_y = max(0, y - EXTRA_SPACE)
                new_h = h + EXTRA_SPACE
                region = tif_image[new_y:new_y + new_h, new_x:new_x + w]

                output_filename = os.path.join(output_dir, f'{file_name}_{output_counter}.jpg')
                cv2.imwrite(output_filename, region)
                output_counter += 1
        
        logging.info(f"Processed {input_file}")

    except Exception as e: 
        print(f"Error while processing {input_file}: {str(e)}")

def main():
    """
    Main function for processing TIFF files in the current directory and saving extracted images.

    Args:
        None

    Returns:
        None
    """
    current_dir = os.getcwd()
    input_dir = current_dir + "\output"
    output_dir = 'output_images'

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    tif_files = glob.glob(os.path.join(input_dir, '*.jpg'))
    for tif_file in tif_files:
        process_tiff_file(tif_file, output_dir)

if __name__ == "__main__":
    main()