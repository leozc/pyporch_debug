"""End-to-end demo: generate a QR code, then detect and decode it."""

import torch

from generate_qr import generate_qr
from detect_qr import detect_qr


def main() -> None:
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    print()

    # Generate a QR code
    message = "Hello from Pants + PyTorch (platform-specific builds)!"
    output_path = "qr_codes/demo.png"
    print(f"Generating QR code with message: {message!r}")
    generate_qr(message, output_path)
    print()

    # Detect and decode the QR code
    print("Detecting QR code...")
    results = detect_qr(output_path)
    print()

    # Verify round-trip
    if results and results[0] == message:
        print("SUCCESS: Round-trip verified — decoded text matches original!")
    else:
        print("FAILURE: Decoded text does not match original.")
        print(f"  Expected: {message!r}")
        print(f"  Got:      {results!r}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
