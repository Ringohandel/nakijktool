import importlib
import sys
import types

import pytest


def load_app(monkeypatch, ocr_text):
    # Mock gradio Interface to prevent launching UI
    gradio = types.ModuleType("gradio")
    class DummyInterface:
        def __init__(self, *args, **kwargs):
            pass
        def launch(self, *args, **kwargs):
            pass
    gradio.Interface = DummyInterface
    class DummyImage:
        def __init__(self, *args, **kwargs):
            pass
    gradio.Image = DummyImage
    monkeypatch.setitem(sys.modules, "gradio", gradio)

    # Mock pytesseract
    pytesseract = types.ModuleType("pytesseract")
    pytesseract.pytesseract = pytesseract
    pytesseract.tesseract_cmd = ""
    def image_to_string(image, lang=None):
        return ocr_text
    pytesseract.image_to_string = image_to_string
    monkeypatch.setitem(sys.modules, "pytesseract", pytesseract)

    # Mock PIL.Image
    pil_pkg = types.ModuleType("PIL")
    pil_image = types.ModuleType("PIL.Image")
    def open_(path):
        return path
    pil_image.open = open_
    pil_pkg.Image = pil_image
    monkeypatch.setitem(sys.modules, "PIL", pil_pkg)
    monkeypatch.setitem(sys.modules, "PIL.Image", pil_image)

    # Import or reload the app after mocks are in place
    if "app" in sys.modules:
        return importlib.reload(sys.modules["app"])
    return importlib.import_module("app")


def test_nakijk_toets_counts(monkeypatch):
    text = "2 J\n3 O\n11 A\n12 C"
    app = load_app(monkeypatch, text)
    result = app.nakijk_toets("dummy.png")
    assert "Aantal goed: 2" in result
    assert "Aantal fout: 2" in result
    assert "Vragen beoordeeld: 4" in result


def test_nakijk_toets_ignores_unknown(monkeypatch):
    text = "1 J\n99 O"
    app = load_app(monkeypatch, text)
    result = app.nakijk_toets("dummy.png")
    assert result.strip() == "Aantal goed: 0\nAantal fout: 0\nVragen beoordeeld: 0"
