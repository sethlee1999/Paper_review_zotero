# Zotero-DOCX Reference Workflow Skills Summary

## Background

This workflow was developed while managing a Word manuscript and a Zotero collection for a wind-engineering literature review. The task involved downloading papers, validating PDFs, inserting Zotero citations into a DOCX manuscript, generating a Zotero bibliography field, and preparing a safe attachment-import script for Zotero.

## Core Skills Identified

### 1. Zotero Collection Audit

Purpose: Read and audit a Zotero collection before modifying documents or attachments.

Key capabilities:
- List all parent bibliographic items in a target Zotero collection.
- Extract Zotero item keys, titles, authors, years, DOIs, URLs, and item types.
- Distinguish parent bibliographic items from child attachments.
- Check whether each Zotero item already has PDF attachments.
- Produce a structured JSON report for downstream matching and verification.

Important practice:
- Use Zotero's local API for read-only inspection.
- Do not modify the Zotero library until the user explicitly confirms.

### 2. DOCX Zotero Citation Insertion

Purpose: Convert plain author-year references in a Word manuscript into live Zotero citation fields.

Key capabilities:
- Inspect DOCX OOXML directly.
- Locate plain-text citation patterns such as `(Breiman, 2001)` or `Amini et al. (2025)`.
- Insert Word field sequences using `ADDIN ZOTERO_ITEM CSL_CITATION`.
- Insert a Zotero bibliography field using `ADDIN ZOTERO_BIBL`.
- Include uncited Zotero items in the bibliography field when the user wants all references listed.
- Preserve manuscript structure and avoid broad rewrites.

Validation:
- Run `unzip -t` on the DOCX.
- Validate `word/document.xml` with `xmllint`.
- Count inserted Zotero citation and bibliography fields.
- Keep a backup before modifying the Word file.

### 3. PDF Download and Verification

Purpose: Download available PDFs and prevent incorrect papers from being attached.

Key capabilities:
- Query DOI/OpenAlex/Semantic Scholar/publisher endpoints for open PDFs.
- Use known open-access endpoints for sources such as CVF, PMLR, NeurIPS, MDPI, Frontiers, Copernicus, arXiv, and selected publisher pages.
- Avoid bypassing paywalls or login restrictions.
- Verify downloaded PDFs by extracting text with `pdftotext`.
- Match extracted title keywords against Zotero metadata.
- Separate verified PDFs from unverified or incorrect candidates.

Important practice:
- Never assume a downloaded PDF is correct based only on filename or search result.
- Keep verified PDFs in one folder and unverified candidates in another.
- Generate a download report listing successful, failed, and unverified items.

### 4. Zotero Attachment Import

Purpose: Attach verified PDFs to their matching Zotero items.

Key capabilities:
- Map each verified PDF to the Zotero parent item key.
- Generate a Zotero internal JavaScript script for attachment import.
- Skip existing matching PDF attachments to avoid duplicates.
- Import only verified PDFs.

Important limitation:
- Zotero's local API supports read-only inspection but rejected direct attachment writes in this workflow.
- The safer approach is to run a generated script inside Zotero via `Tools -> Developer -> Run JavaScript`.
- Avoid directly editing Zotero's SQLite database.

### 5. Safety and Reproducibility

Purpose: Keep the workflow auditable and reversible.

Key capabilities:
- Create backups before modifying DOCX files.
- Keep structured reports under `data/`.
- Keep generated scripts in the project root.
- Record which PDFs were verified and which were not found.
- Avoid destructive or irreversible Zotero changes unless explicitly confirmed.

## Suggested Reusable Skill

Name: `zotero-docx-reference-manager`

Purpose:
Manage Zotero-backed references for academic DOCX manuscripts, including citation insertion, bibliography generation, PDF download, PDF verification, and Zotero attachment import script generation.

Inputs:
- Zotero collection key or collection name.
- Target DOCX manuscript path.
- Optional output folder for downloaded PDFs.

Outputs:
- Updated DOCX with live Zotero citation and bibliography fields.
- Verified PDF folder.
- Unverified candidate PDF folder.
- JSON download/verification report.
- Zotero JavaScript attachment-import script.

Safety rules:
- Use Zotero local API only for read-only inspection unless a writable API is explicitly available and confirmed.
- Never attach unverified PDFs.
- Never bypass paywalls.
- Never edit Zotero SQLite directly by default.
- Always preserve a DOCX backup before OOXML edits.

## Files Produced in This Workflow

- `Manuscript_Final_Polished.docx`: updated DOCX with Zotero citation and bibliography fields.
- `downloaded_papers/`: verified downloaded PDFs.
- `downloaded_papers_unverified/`: incorrect or unverified PDF candidates.
- `data/download_report_verified.json`: verification report.
- `attach_pdfs_to_zotero.js`: Zotero-side script for attaching verified PDFs.
