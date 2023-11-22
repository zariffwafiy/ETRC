import glob, fitz
import os
import shutil
from pathlib import Path

# To get better resolution
zoom_x = 2.0  # horizontal zoom
zoom_y = 2.0  # vertical zoom
mat = fitz.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension

path = 'data/'
all_files = glob.glob(path + "*.pdf")

output_dir = "output"
input_dir = os.getcwd()

if os.path.exists(output_dir):
    shutil.rmtree(output_dir)
    
os.makedirs(output_dir, exist_ok=True)

for filename in all_files:
    doc = fitz.open(filename)
    for page in doc:  # iterate through the pages
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        x = page.number+1
        p = Path(filename).stem #get filename without path
        p_str = str(p)
        pix.save(f"{output_dir}/{p_str}_page_{x}.jpg")
