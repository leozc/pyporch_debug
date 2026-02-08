"""Detect and decode QR codes from images using qreader (YOLOv8 + PyTorch)."""

import sys

import cv2
from qreader import QReader


def detect_qr(image_path: str) -> list[str]:
    """Detect and decode QR codes in an image.

    Args:
        image_path: Path to the image containing QR codes.

    Returns:
        List of decoded text strings from detected QR codes.
    """
    qreader = QReader()
    image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
    decoded = qreader.detect_and_decode(image=image)
    results = [text for text in decoded if text is not None]
    print(f"Detected {len(results)} QR code(s) in {image_path}:")
    for i, text in enumerate(results):
        print(f"  [{i + 1}] {text}")
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: detect_qr.py <image_path>")
        sys.exit(1)
    detect_qr(sys.argv[1])
