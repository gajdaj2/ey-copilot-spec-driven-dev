"""Testy środowiska startowego — sprawdzają, że repozytorium jest gotowe do pracy.

Testy aplikacji dopisujemy w trakcie dnia (Blok 2–3).
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE_DOCS = ROOT / "data" / "sample_docs"


def test_python_version():
    assert sys.version_info >= (3, 12)


def test_core_dependencies_installed():
    import fastapi  # noqa: F401
    import uvicorn  # noqa: F401


def test_sample_docs_present_and_utf8():
    docs = sorted(SAMPLE_DOCS.glob("*.md"))
    assert len(docs) >= 5
    for doc in docs:
        text = doc.read_text(encoding="utf-8")
        assert "fikcyjn" in text.lower(), f"{doc.name}: brak oznaczenia danych fikcyjnych"


def test_env_example_has_names_only():
    for line in (ROOT / ".env.example").read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            name, _, value = line.partition("=")
            assert value == "", f"{name}: .env.example nie może zawierać wartości"


def test_env_is_ignored_by_git():
    result = subprocess.run(  # noqa: S603
        ["git", "check-ignore", "-q", ".env"],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
    )
    assert result.returncode == 0, ".env musi być w .gitignore"
