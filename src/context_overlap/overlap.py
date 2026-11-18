from __future__ import annotations

import json
import re
from pathlib import Path

TOKEN = re.compile(r"[a-zA-ZáéíóúñÁÉÍÓÚÑ0-9]+")


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in TOKEN.findall(text)]


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def load_docs(docs_dir: Path) -> dict[str, str]:
    return {p.stem: p.read_text(encoding="utf-8") for p in sorted(docs_dir.glob("*.txt"))}


def best_context(docs: dict[str, str], question: str) -> tuple[str, str, float]:
    q = set(tokenize(question))
    ranked = []
    for doc_id, text in docs.items():
        score = jaccard(q, set(tokenize(text)))
        ranked.append((score, doc_id, text))
    ranked.sort(reverse=True)
    score, doc_id, text = ranked[0]
    return doc_id, text, score


def analyze_case(question: str, answer: str, docs: dict[str, str]) -> dict:
    doc_id, context, q_ctx = best_context(docs, question)
    q = set(tokenize(question))
    c = set(tokenize(context))
    a = set(tokenize(answer))
    return {
        "question": question,
        "doc_id": doc_id,
        "question_context": round(q_ctx, 4),
        "answer_context": round(jaccard(a, c), 4),
        "question_answer": round(jaccard(q, a), 4),
        "answer": answer,
    }


def run_lab(cases_path: Path, docs_dir: Path) -> dict:
    docs = load_docs(docs_dir)
    cases = [json.loads(l) for l in cases_path.read_text(encoding="utf-8").splitlines() if l.strip()]
    details = [analyze_case(c["question"], c["answer"], docs) for c in cases]
    avg = {
        "question_context": round(sum(d["question_context"] for d in details) / len(details), 4),
        "answer_context": round(sum(d["answer_context"] for d in details) / len(details), 4),
        "question_answer": round(sum(d["question_answer"] for d in details) / len(details), 4),
    }
    return {"avg": avg, "details": details, "score": avg["answer_context"]}
