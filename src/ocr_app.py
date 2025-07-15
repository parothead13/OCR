import re
from typing import Tuple

try:
    from PIL import Image, ImageOps, ImageEnhance
except ImportError:  # pragma: no cover - Pillow not installed
    Image = None

try:
    import pytesseract
except ImportError:  # pragma: no cover - pytesseract not installed
    pytesseract = None


def load_image(path: str):
    """Load an image from a file path."""
    if Image is None:
        raise RuntimeError("Pillow is required but not installed")
    return Image.open(path)


def enhance_contrast(image) -> 'Image.Image':
    """Enhance image contrast to aid OCR."""
    if ImageOps is None:
        raise RuntimeError("Pillow is required but not installed")
    # autocontrast maximises contrast based on image histogram
    enhanced = ImageOps.autocontrast(image)
    return enhanced


def run_ocr(image) -> str:
    """Run OCR on the provided image."""
    if pytesseract is None:
        raise RuntimeError("pytesseract is required but not installed")
    return pytesseract.image_to_string(image)


def find_xl(text: str) -> Tuple[bool, int]:
    """Return whether 'XL' appears in text and how many times."""
    matches = re.findall(r"xl", text, flags=re.IGNORECASE)
    return bool(matches), len(matches)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OCR XL detector")
    parser.add_argument("image", help="Path to image file")
    args = parser.parse_args()

    img = load_image(args.image)
    img = enhance_contrast(img)
    text = run_ocr(img)
    found, count = find_xl(text)
    if found:
        print(f"Found {count} occurrence(s) of 'XL'.")
    else:
        print("No 'XL' found.")
