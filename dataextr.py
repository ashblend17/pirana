import pytesseract
from PIL import Image

# Load the image
image = Image.open('image.png')

# Use Tesseract OCR to extract text
text = pytesseract.image_to_string(image)

# Print the extracted text
print(text)
