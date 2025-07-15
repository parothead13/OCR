# OCR XL Detector

This command-line application loads an image, maximizes its contrast,
performs OCR using `pytesseract` and reports the number of occurrences
of the contiguous letters `XL` (case-insensitive).

```
python -m src.ocr_app path/to/image.png
```

The script requires `Pillow` and `pytesseract` to be installed and
`pytesseract` needs access to a Tesseract OCR binary.
