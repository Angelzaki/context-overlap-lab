from pathlib import Path

from context_overlap.overlap import run_lab

ROOT = Path(__file__).resolve().parents[1]


def test_overlap_report():
    report = run_lab(ROOT / "samples" / "cases.jsonl", ROOT / "samples" / "docs")
    assert "avg" in report
    assert report["avg"]["answer_context"] >= 0.2
    assert len(report["details"]) == 3
