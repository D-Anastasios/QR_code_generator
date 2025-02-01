import qrcode
from PIL import Image
import argparse

"""
------------------------------------------------------
QR Code Generator for Email Contact
------------------------------------------------------
Author: Anastasios Dadiotis
Created: February 1, 2025
Last Modified: February 1, 2025
Description:
    This script generates a QR code that opens a pre-filled email 
    when scanned. The QR code includes a recipient email address, 
    subject, and an optional body message. A logo can be embedded 
    at the center of the QR code.
    
Usage:
    As a standalone script (command-line mode):
        python generate_qr.py --email "example@email.com" --subject "Study Participation" --logo "logo.png"

    With an optional body message:
        python generate_qr.py --email "example@email.com" --subject "Study Participation" --logo "logo.png" --body "I'm interested."

    As an imported function in another script:
        from generate_qr import generate_qr_code
        generate_qr_code("example@email.com", "Study Participation", "logo.png")

Requirements:
    - Python 3.x
    - qrcode (pip install qrcode[pil])
    - PIL (Pillow) for image processing (pip install pillow)

------------------------------------------------------
"""

def generate_qr_code(email, subject, logo_path, body=None, output_file="email_qr.png"):
    """
    Generates a QR code for an email link and embeds a logo in the center.

    Parameters:
        email (str): The recipient email address.
        subject (str): The subject of the email.
        logo_path (str): Path to the logo image (PNG or JPG).
        body (str, optional): The email body. Defaults to a French recruitment message.
        output_file (str, optional): The name of the output QR code image file.

    Returns:
        None. The QR code is saved as an image file and displayed.

    Example Usage:
        generate_qr_code("test@example.com", "Participation", "logo.png")
    """

    # Default body text in French
    if body is None:
        body = ("Je suis intéressé(e) à participer à votre étude. "
                "Vous pouvez me contacter à cette adresse e-mail ou "
                "m'appeler au [votre numéro].")

    # Encode the email link
    email_link = f"mailto:{email}?subject={subject}&body={body}"

    # QR code configuration
    qr = qrcode.QRCode(
        version=6,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction to support logo
        box_size=10,
        border=4
    )

    # Add email data to QR Code
    qr.add_data(email_link)
    qr.make(fit=True)

    # Create QR code image with colors
    qr_img = qr.make_image(fill_color="blue", back_color="white").convert("RGB")

    # Try adding the logo
    try:
        logo = Image.open(logo_path)

        # Resize logo (make it ~25% of QR code size)
        max_logo_size = qr_img.size[0] // 3  # Adjust size (1/3 of QR width)
        logo = logo.resize((max_logo_size, max_logo_size))

        # Calculate position to center the logo
        pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)

        # Paste logo onto QR code
        qr_img.paste(logo, pos)

    except FileNotFoundError:
        print("Logo file not found. Proceeding without a logo.")

    # Save and show QR code
    qr_img.save(output_file)
    qr_img.show()
    print(f"QR code saved as {output_file}")

def main():
    """
    Parses command-line arguments and generates a QR code.
    
    Arguments:
        --email (str)    : Recipient email address (required)
        --subject (str)  : Email subject (required)
        --logo (str)     : Path to the logo image (required)
        --body (str)     : Optional email body message
        --output (str)   : Output filename for the QR code (default: email_qr.png)

    Example Command-Line Usage:
        python generate_qr.py --email "test@example.com" --subject "Participation" --logo "logo.png"
    """

    parser = argparse.ArgumentParser(description="Generate a QR code for an email with an embedded logo.")

    # Required arguments
    parser.add_argument("--email", required=True, help="Recipient email address")
    parser.add_argument("--subject", required=True, help="Subject of the email")
    parser.add_argument("--logo", required=True, help="Path to the logo image")

    # Optional argument
    parser.add_argument("--body", default=None, help="Email body (default: French recruitment text)")
    parser.add_argument("--output", default="email_qr.png", help="Output filename for the QR code image")

    args = parser.parse_args()

    # Call function with provided arguments
    generate_qr_code(args.email, args.subject, args.logo, args.body, args.output)

# Run main() only if script is executed directly
if __name__ == "__main__":
    main()
