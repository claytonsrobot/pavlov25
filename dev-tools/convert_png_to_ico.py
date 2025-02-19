# pip install pillow
####    
import argparse
from PIL import Image
from pathlib import Path

def convert_png_to_ico(png_file_path, ico_file_path):
    # Open the PNG file
    img = Image.open(png_file_path)

    # Convert the image to ICO format and save it
    img.save(ico_file_path, format='ICO')
    print(f"Converted {png_file_path} to {ico_file_path}")

def main():
    parser = argparse.ArgumentParser(description='Convert a PNG file to an ICO file.')
    parser.add_argument('input', type=Path, help='Path to the input PNG file')
    parser.add_argument('output', type=Path, help='Path to the output ICO file')
    
    args = parser.parse_args()
    
    convert_png_to_ico(args.input, args.output)

if __name__ == "__main__":
    main()
    
#else:
#    # example usage 
#    convert_png_to_ico(args.input, args.output)

