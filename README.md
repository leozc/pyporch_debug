# Platform-Specific PyTorch with Pants

Demo project testing Pants' ability to use **different PyTorch packages per platform**:

- **Linux** — CPU-only torch (from `download.pytorch.org/whl/cpu`)
- **macOS** — Full torch from standard PyPI

Uses [qreader](https://github.com/Eric-Canas/qreader) (YOLOv8/PyTorch) for QR code detection as the demo workload.

## How It Works

Pants' `[python-repos].indexes` is global, so we use **two resolves** (`linux`, `macos`) with `parametrize()`:

1. Both PyPI and CPU-only indexes are listed globally
2. Each resolve has its own lockfile (`linux.lock`, `macos.lock`)
3. The Linux lockfile locks `torch==2.10.0+cpu`; the macOS lockfile locks `torch==2.10.0` (full)
4. All source and binary targets are parametrized across both resolves

## Prerequisites

```bash
# Linux: needed by pyzbar for QR decoding
sudo apt-get install libzbar0
```

- Python 3.12
- Pants 2.30.0 (auto-installed)

## Running

```bash
# End-to-end demo: generate QR, detect it, verify round-trip
pants run //:demo@resolve=linux     # Linux (CPU-only torch)
pants run //:demo@resolve=macos     # macOS (full torch)

# Individual scripts
pants run //:generate@resolve=linux              # Generate a QR code
pants run //:detect@resolve=linux -- image.png   # Detect QR from image
```

## Lockfile Generation

```bash
# Linux: both indexes available, CPU-only torch wins (local version sorts higher)
pants generate-lockfiles --resolve=linux

# macOS: override indexes to exclude CPU-only, so standard PyPI torch is locked
pants --python-repos-indexes='["https://pypi.org/simple/"]' generate-lockfiles --resolve=macos
```

## Project Structure

```
pants.toml                          # Build config: two resolves, dual indexes
BUILD                               # python_sources + pex_binary targets (parametrized)
generate_qr.py                      # Generate QR codes from text
detect_qr.py                        # Detect/decode QR codes (qreader + YOLOv8)
demo_qr.py                          # End-to-end round-trip demo
3rdparty/python/
  requirements.txt                  # torch, torchvision, qreader, qrcode[pil], opencv-python
  BUILD                             # python_requirements with parametrize
  linux.lock                        # Lockfile with CPU-only torch
  macos.lock                        # Lockfile with full PyPI torch
```
