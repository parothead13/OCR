# OCR XL Detector

This command-line application loads an image, maximizes its contrast,
performs OCR using AWS Rekognition and reports the number of occurrences
of the contiguous letters `XL` (case-insensitive).

```
python -m src.ocr_app path/to/image.png
```

The script requires `Pillow` and `boto3` to be installed and
valid AWS credentials with access to the Rekognition API.

AWS operations require a region. The application will look for the
`AWS_REGION` or `AWS_DEFAULT_REGION` environment variable and defaults to
`us-east-1` when none is specified.
