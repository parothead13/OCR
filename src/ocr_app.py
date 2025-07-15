import re
from typing import Tuple

try:
    from PIL import Image, ImageOps, ImageEnhance
except ImportError:  # pragma: no cover - Pillow not installed
    Image = None

try:
    import boto3
except ImportError:  # pragma: no cover - boto3 not installed
    boto3 = None


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
    """Run OCR on the provided image using AWS Rekognition."""
    if boto3 is None:
        raise RuntimeError("boto3 is required but not installed")
    import io

    buffer = io.BytesIO()
    fmt = image.format or "PNG"
    image.save(buffer, format=fmt)
    image_bytes = buffer.getvalue()

    client = boto3.client("rekognition")
    response = client.detect_text(Image={"Bytes": image_bytes})
    detections = response.get("TextDetections", [])
    text = " ".join(d.get("DetectedText", "") for d in detections)
    return text


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
