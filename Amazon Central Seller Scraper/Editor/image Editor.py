# Importing the PIL library
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


def image_editor(product_text: str, product_quantity: str):
    # Open an Image
    img = Image.open('image.jpg')

    # Call draw Method to add 2D graphics in an image
    draw = ImageDraw.Draw(img)

    # Define font
    font = ImageFont.truetype("arial.ttf", 65)
    quantity_font = ImageFont.truetype("arial.ttf", 150)

    # Define text
    text = product_text
    quantity = product_quantity
    # Calculate center position of the image
    img_width, img_height = img.size
    center_x = img_width / 2
    center_y = img_height / 2

    # Calculate center position of the text
    text_width, text_height = draw.textsize(text, font=font)
    text_x = center_x - text_width / 2
    text_y = center_y - text_height / 2

    # Add Text to an image
    draw.text((text_x, 50), text, fill=(0, 0, 0), font=font)

    # Add Text to an image on the bottom right
    draw.text((1080, 440), quantity, fill=(0, 0, 0), font=quantity_font)

    # Display edited image
    img.show()

    # Save the edited image
    img.save("edited_image.jpg")


image_editor("Perennial Lily Flowering Bulbs", "2")



import win32print
from PIL import Image

# Open the image file
img = Image.open("edited_image.jpg")

# Get the printer name
printer_name = win32print.GetDefaultPrinter()

# Print the image
hDC = win32print.OpenPrinter(printer_name)
try:
    # Start a new print job
    hJob = win32print.StartDocPrinter(hDC, 1, ("edited_image.jpg", None, "RAW"))
    try:
        # Start a new page
        win32print.StartPagePrinter(hDC)
        # Send the image to the printer
        img_data = img.tobytes()
        win32print.WritePrinter(hDC, img_data)
        # End the page
        win32print.EndPagePrinter(hDC)
    finally:
        # End the print job
        win32print.EndDocPrinter(hDC)
finally:
    # Close the printer handle
    win32print.ClosePrinter(hDC)
