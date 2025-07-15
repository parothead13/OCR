import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))

from ocr_app import find_xl, main


def test_find_xl_detects_case_insensitive():
    found, count = find_xl('xxl XL xl')
    assert found
    assert count == 3


def test_find_xl_no_match():
    found, count = find_xl('Hello world')
    assert not found
    assert count == 0


def test_main_processes_directory(tmp_path, monkeypatch):
    images = tmp_path / "imgs"
    images.mkdir()
    (images / "one.png").write_text("data")
    (images / "two.jpg").write_text("data")

    def fake_process(path):
        if path.endswith("one.png"):
            return True, 2
        return False, 0

    monkeypatch.setattr("ocr_app.process_image_file", fake_process)
    csv_file = tmp_path / "out.csv"
    main([str(images), "--csv", str(csv_file)])

    import csv

    with open(csv_file, newline="") as fh:
        rows = list(csv.DictReader(fh))

    assert any(row["file"].endswith("one.png") and row["found"] == "True" and row["count"] == "2" for row in rows)
    assert any(row["file"].endswith("two.jpg") and row["found"] == "False" and row["count"] == "0" for row in rows)

