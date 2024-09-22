import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# Load the image
image_path = 'fifthtext.png'  # Replace with your image path

def extract_characters_from_image(image_path):
    # Load the image
    img = Image.open(image_path)
    
    # Use Tesseract to do OCR on the image
    text = pytesseract.image_to_string(img, config='--psm 6')

    # Filter to get only 'A' and 'B' characters
    filtered_text = ''.join(c for c in text if c in 'AB')
    
    # Return the recognized text
    # return filtered_text
    return filtered_text[-1]

extracted_text = extract_characters_from_image(image_path)
print(extracted_text)
