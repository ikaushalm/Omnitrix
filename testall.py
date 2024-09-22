from PIL import Image
import pytesseract  




pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"





image_path = 'fifthtext.png'  # Replace with your image path

from PIL import Image
import pytesseract

def extract_characters_from_image(image_path):
    # Load the image
    img = Image.open(image_path)

    # Convert image to RGB and extract pixels
    pixels = img.load()
    width, height = img.size

    recognized_characters = []

    # Iterate through pixels to detect red and blue areas
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r > 150 and g < 100 and b < 100:  # Red detection
                recognized_characters.append('B')
            elif r < 100 and g < 100 and b > 150:  # Blue detection
                recognized_characters.append('A')

    # Return the last recognized character
    if recognized_characters:
        return recognized_characters[-1]
    else:
        # Fallback to OCR if no colors were detected
        text = pytesseract.image_to_string(img, config='--psm 6')
        filtered_text = ''.join(c for c in text if c in 'AB')
        return filtered_text[-1] if filtered_text else None


print(extract_characters_from_image(image_path))