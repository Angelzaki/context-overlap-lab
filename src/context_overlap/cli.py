from __future__ import annotations

import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from context_overlap.overlap import run_lab

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="context-overlap")
    parser.add_argument("--cases", default="samples/cases.jsonl")
    parser.add_argument("--docs", default="samples/docs")
    parser.add_argument("--results", default="results")
    args = parser.parse_args(argv)

    report = run_lab(Path(args.cases), Path(args.docs))
    out = Path(args.results)
    out.mkdir(parents=True, exist_ok=True)
    (out / "overlap_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    table = Table(title="Context Overlap Lab")
    table.add_column("metric")
    table.add_column("avg", justify="right")
    for k, v in report["avg"].items():
        table.add_row(k, f"{v:.0%}")
    console.print(table)
    console.print(f"score(answer_context): [bold]{report['score']:.0%}[/bold]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
