# Platform-Specific PyTorch with Pants

Demo project testing Pants' ability to use **different PyTorch packages per platform**:

- **Linux** — CPU-only torch (from `download.pytorch.org/whl/cpu`)
- **macOS** — Full torch from standard PyPI

Uses [qreader](https://github.com/Eric-Canas/qreader) (YOLOv8/PyTorch) for QR code detection as the demo workload.

## How It Works

Pants 2.30.1's `resolves_to_sources` scopes a **named index** to specific packages on specific platforms — all within a single resolve and lockfile:

```toml
[python-repos]
indexes = [
  "https://pypi.org/simple/",
  "pytorch_cpu=https://download.pytorch.org/whl/cpu",
]

[python.resolves_to_sources]
python-default = [
    "pytorch_cpu=torch; sys_platform == 'linux'",
    "pytorch_cpu=torchvision; sys_platform == 'linux'",
]
```

- The `pytorch_cpu` index is only used for `torch` and `torchvision`, and only on Linux
- On macOS, those packages resolve from PyPI (full torch with Metal support)
- One lockfile (`default.lock`) contains both platform variants; the correct one is selected at install time

## Prerequisites

```bash
# Linux: needed by pyzbar for QR decoding
sudo apt-get install libzbar0
```

- Python 3.12
- Pants 2.30.1 (auto-installed)

## Running

```bash
# End-to-end demo: generate QR, detect it, verify round-trip
pants run //:demo

# Individual scripts
pants run //:generate              # Generate a QR code
pants run //:detect -- image.png   # Detect QR from image
```

## Lockfile Generation

```bash
pants generate-lockfiles
```

## Project Structure

```
pants.toml                          # Build config: resolves_to_sources for platform-specific torch
BUILD                               # python_sources + pex_binary targets
generate_qr.py                      # Generate QR codes from text
detect_qr.py                        # Detect/decode QR codes (qreader + YOLOv8)
demo_qr.py                          # End-to-end round-trip demo
3rdparty/python/
  requirements.txt                  # torch, torchvision, qreader, qrcode[pil], opencv-python
  BUILD                             # python_requirements target
  default.lock                      # Universal lockfile (CPU-only torch for Linux, full for macOS)
```
