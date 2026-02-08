"""Generate QR codes from text input."""

import os
import sys

import qrcode


def generate_qr(text: str, output_path: str) -> str:
    """Generate a QR code image from text.

    Args:
        text: The text to encode in the QR code.
        output_path: Path to save the QR code image.

    Returns:
        The path to the saved image.
    """
    img = qrcode.make(text)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    img.save(output_path)
    print(f"QR code saved to {output_path}")
    return output_path


if __name__ == "__main__":
    text = sys.argv[1] if len(sys.argv) > 1 else "Hello from Pants + PyTorch!"
    output = sys.argv[2] if len(sys.argv) > 2 else "qr_codes/output.png"
    generate_qr(text, output)
