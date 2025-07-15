import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from ocr_app import find_xl


def test_find_xl_detects_case_insensitive():
    found, count = find_xl('xxl XL xl')
    assert found
    assert count == 3


def test_find_xl_no_match():
    found, count = find_xl('Hello world')
    assert not found
    assert count == 0
