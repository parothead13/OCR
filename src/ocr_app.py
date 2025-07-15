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

    import os

    region = (
        os.environ.get("AWS_REGION")
        or os.environ.get("AWS_DEFAULT_REGION")
        or "us-east-1"
    )
    client = boto3.client("rekognition", region_name=region)
    response = client.detect_text(Image={"Bytes": image_bytes})
    detections = response.get("TextDetections", [])
    text = " ".join(d.get("DetectedText", "") for d in detections)
    return text


def find_xl(text: str) -> Tuple[bool, int]:
    """Return whether 'XL' appears in text and how many times."""
    matches = re.findall(r"xl", text, flags=re.IGNORECASE)
    return bool(matches), len(matches)


def process_image_file(path: str) -> Tuple[bool, int]:
    """Process a single image file and return XL detection results."""
    img = load_image(path)
    img = enhance_contrast(img)
    text = run_ocr(img)
    return find_xl(text)


def main(argv=None) -> None:
    """Entry point for command-line execution."""
    import argparse
    import csv
    from pathlib import Path

    parser = argparse.ArgumentParser(description="OCR XL detector")
    parser.add_argument("path", help="Path to image file or directory")
    parser.add_argument("--csv", dest="csv_path", help="Write results to CSV")
    args = parser.parse_args(argv)

    p = Path(args.path)
    if p.is_dir():
        files = [f for f in p.iterdir() if f.is_file() and f.suffix.lower() in {".png", ".jpg", ".jpeg"}]
    else:
        files = [p]

    results = []
    for file in files:
        found, count = process_image_file(str(file))
        results.append({"file": str(file), "found": found, "count": count})

    if args.csv_path:
        with open(args.csv_path, "w", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["file", "found", "count"])
            writer.writeheader()
            writer.writerows(results)
    else:
        for row in results:
            if row["found"]:
                print(f"{row['file']}: Found {row['count']} occurrence(s) of 'XL'.")
            else:
                print(f"{row['file']}: No 'XL' found.")


if __name__ == "__main__":
    main()
