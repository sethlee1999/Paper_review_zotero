---
name: zotero-docx-reference-manager
description: Use when managing Zotero-backed references for an academic Word DOCX manuscript: read a Zotero collection, download and verify PDFs, convert plain author-year citations into live Zotero citation fields, insert/update a Zotero bibliography field, generate a Zotero JavaScript attachment-import script, or audit which references/PDFs are missing. Trigger on Zotero, DOCX citation insertion, bibliography generation, PDF download/verification, Zotero attachments, manuscript references, or literature-review reference cleanup.
---

# Zotero DOCX Reference Manager

Use this skill for workflows that connect a Zotero collection to a Word manuscript.

## Safety Rules

- Treat Zotero library writes as explicit-confirmation actions.
- Use Zotero local API for read-only collection/item/attachment inspection.
- Do not edit Zotero SQLite directly by default.
- Do not bypass paywalls, logins, or subscription controls.
- Never attach a PDF unless it was verified against the Zotero item metadata.
- Back up the DOCX before OOXML edits.
- Validate edited DOCX files with `unzip -t` and `xmllint` on `word/document.xml`.

## Standard Workflow

1. Identify the target Zotero collection and target DOCX.
2. Export Zotero parent-item metadata to JSON: key, title, item type, creators, year, DOI, URL.
3. Inspect existing child attachments for each item and avoid duplicates.
4. Download openly available PDFs only.
5. Verify PDFs with `scripts/verify_downloaded_pdfs.py`; move or report unverified candidates separately.
6. Insert live Zotero citation fields into the DOCX where plain author-year citations can be confidently matched.
7. Insert one Zotero bibliography field. If the user wants all collection items listed, include collection items as `uncited` citation items in the bibliography field.
8. Generate a Zotero-side JavaScript attachment script for verified PDFs. The user runs it in Zotero via `Tools -> Developer -> Run JavaScript`.
9. Report counts: collection items, matched citations, bibliography items, verified PDFs, unverified PDFs, and not-found PDFs.

## DOCX Citation Notes

Insert normal Word field sequences:

- `w:fldChar w:fldCharType="begin"`
- `w:instrText xml:space="preserve"` with `ADDIN ZOTERO_ITEM CSL_CITATION <json>`
- `w:fldChar w:fldCharType="separate"`
- visible citation text
- `w:fldChar w:fldCharType="end"`

For bibliography, use `ADDIN ZOTERO_BIBL <json>`.

Prefer minimal OOXML edits. Do not rewrite the whole document XML with namespace-renaming tools.

## Zotero Attachment Notes

If Zotero local API rejects writes, generate a JavaScript file from `scripts/attach_pdfs_to_zotero.template.js`.

The generated script should:

- Use Zotero parent item keys.
- Import only verified PDF paths.
- Skip existing same-title PDF attachments.
- Return a line-by-line status summary.

## Bundled Scripts

- `scripts/verify_downloaded_pdfs.py`: verifies PDF text against Zotero metadata and writes a JSON report.
- `scripts/attach_pdfs_to_zotero.template.js`: template for a Zotero Run JavaScript attachment importer.
