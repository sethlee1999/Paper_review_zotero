#!/usr/bin/env python3
"""Verify downloaded PDFs against Zotero item metadata.

Input:
  --zotero-json data/zotero_references.json
  --pdf-dir downloaded_papers
  --out data/download_report_verified.json

The Zotero JSON should be a list of Zotero API item objects. PDF filenames should
start with the Zotero item key, for example KEY_Title.pdf.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


STOPWORDS = {
    "the",
    "a",
    "an",
    "of",
    "and",
    "for",
    "in",
    "to",
    "using",
    "with",
    "on",
    "from",
    "based",
    "new",
    "review",
    "method",
    "system",
    "approach",
    "applications",
    "application",
    "learning",
    "machine",
    "deep",
    "artificial",
    "intelligence",
}


def title_keywords(title: str) -> list[str]:
    return [
        word
        for word in re.findall(r"[a-z0-9]+", title.lower())
        if len(word) > 2 and word not in STOPWORDS
    ]


def extract_pdf_text(pdf: Path, pages: int) -> str:
    output = subprocess.check_output(
        ["pdftotext", "-f", "1", "-l", str(pages), str(pdf), "-"],
        stderr=subprocess.DEVNULL,
        timeout=20,
    )
    return output.decode("utf-8", "ignore").lower()


def verify_pdf(pdf: Path, title: str, pages: int, threshold: float) -> tuple[bool, dict]:
    keywords = title_keywords(title)
    if not keywords:
        return False, {"reason": "no_title_keywords", "hits": 0, "total": 0, "ratio": 0.0}

    try:
        text = extract_pdf_text(pdf, pages)
    except Exception as exc:  # noqa: BLE001
        return False, {"reason": f"text_extract_failed: {exc}", "hits": 0, "total": len(keywords), "ratio": 0.0}

    hits = sum(1 for word in keywords if word in text)
    ratio = hits / max(1, len(keywords))
    return ratio >= threshold, {"reason": "ok" if ratio >= threshold else "low_title_match", "hits": hits, "total": len(keywords), "ratio": ratio}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--zotero-json", required=True)
    parser.add_argument("--pdf-dir", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--pages", type=int, default=3)
    parser.add_argument("--threshold", type=float, default=0.45)
    args = parser.parse_args()

    items = json.loads(Path(args.zotero_json).read_text())
    pdf_dir = Path(args.pdf_dir)
    report = []

    for item in items:
        data = item.get("data", item)
        key = data["key"]
        title = data.get("title", "")
        pdfs = sorted(pdf_dir.glob(f"{key}_*.pdf"))
        if not pdfs:
            report.append({"key": key, "title": title, "status": "not_downloaded", "file": ""})
            continue

        verified = []
        rejected = []
        for pdf in pdfs:
            ok, detail = verify_pdf(pdf, title, args.pages, args.threshold)
            entry = {"file": str(pdf), **detail}
            if ok:
                verified.append(entry)
            else:
                rejected.append(entry)

        if verified:
            report.append({"key": key, "title": title, "status": "downloaded_verified", "file": verified[0]["file"], "rejected": rejected})
        else:
            report.append({"key": key, "title": title, "status": "unverified", "file": "", "rejected": rejected})

    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print(f"verified={sum(row['status'] == 'downloaded_verified' for row in report)}")
    print(f"not_verified={sum(row['status'] != 'downloaded_verified' for row in report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
