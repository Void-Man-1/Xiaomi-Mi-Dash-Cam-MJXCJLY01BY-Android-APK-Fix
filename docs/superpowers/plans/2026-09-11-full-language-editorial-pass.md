# Full Language Editorial Pass Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make all public-facing non-README copy read naturally and professionally in English, Polish, Ukrainian, German, and Russian without changing technical facts, compatibility claims, release identity, or repository behavior.

**Architecture:** Work on `language/full-editorial-pass-2026-09-11`. Review each public text surface against the approved editorial standard, edit only prose that is awkward or inconsistent, preserve machine-sensitive identifiers/URLs/markers, and validate the result with repository integrity checks, a strict no-README-diff gate, HTML/JSON-LD parsing, terminology scans, and browser layout checks.

**Tech Stack:** Static HTML, Markdown, GitHub issue forms (YAML), GitHub Actions YAML/Python snippets, Python 3 validators, GitHub Actions, browser/Chrome verification where needed.

**Spec:** `docs/superpowers/specs/2026-09-11-full-language-editorial-pass-design.md`

## Global Constraints

- Do not modify any file whose basename is `README.md` or `README.<locale>.md`; all README files must remain byte-for-byte identical to `main`.
- Do not modify the published `v2.0.0` APK, release asset, checksum, signing identity, package/version metadata, model identifiers, evidence files, test results, or URLs.
- Do not broaden compatibility claims or weaken caveats. Android 10 and 11 remain untested; firmware OTA remains outside acceptance; `MJXCJLY02BY` remains unsupported/unclaimed.
- Preserve technical terms and identifiers where translation would be wrong: APK, Android, HyperOS, Wi-Fi, SHA-256, RTSP, ARM64, ARMv7, GitHub, package names, hashes, model codes, code identifiers, workflow markers, and release URLs.
- Russian remains last in the language selector and has no flag image.
- Edit for native readability, not literal equivalence. Prefer restrained support/documentation language over slogans, bureaucratic prose, or machine-translated phrasing.
- Do not rewrite historical spec/plan records for style unless a current instruction would otherwise mislead readers.

---

### Task 1: Inventory public text and freeze the no-README baseline

**Files:**
- Read: repository tree on `main` and language branch
- Read: all `README*` files for hash comparison only
- Read: all public non-README `.md`, `.html`, `.yml`, and relevant workflow text
- Create/modify only if needed: `tools/verify_repository_integrity.py`

**Interfaces:**
- Consumes: approved spec and current `main`.
- Produces: explicit edit inventory plus a mechanical guard against README changes.

- [ ] **Step 1: Record every README blob SHA from `main`**

Expected invariant: the language branch retains the same blob SHA for every repository file matching `README.md` or `README.*.md`, including README files in subdirectories.

- [ ] **Step 2: Inventory public non-README prose**

Review at minimum:

```text
site/index.html
site/pl/index.html
site/uk/index.html
site/de/index.html
site/ru/index.html
.github/ISSUE_TEMPLATE/bug_report.yml
CONTRIBUTING.md
NOTICE.md
docs/AUDIT_2026-09-11.md
docs/GITHUB_LISTING.md
docs/PUBLISHING_CHECKLIST.md
docs/RELEASE_NOTES_2.0.0.md
docs/REVERSE_ENGINEERING_REPORT.md
docs/TEST_REPORT_2.0.0.md
docs/TROUBLESHOOTING.md
source-kit/PATCH_SOURCE_NOTICES.md
source-kit/docs/BUILD_FROM_ORIGINAL.md
source-kit/docs/LICENSING.md
source-kit/docs/PATCH_MAP.md
.github/workflows/update-readme-download.yml
```

Do not edit README-named evidence/source-kit/release-assets files even when their prose could be improved.

- [ ] **Step 3: Define terminology residues to eliminate where appropriate**

Examples to check rather than blindly replace:

```text
canonical APK
physically hardware accepted
live preview / Mi Account / European region in localized prose
final signed APK / final signierte APK-style calques
literal “proof” or “verification” slogans where ordinary wording is clearer
```

- [ ] **Step 4: Commit only if a durable validator change is required**

If the existing integrity validator can enforce the final invariants without becoming an editorial style checker, leave it unchanged.

### Task 2: Edit the English public surfaces

**Files:**
- Modify as findings justify: `site/index.html`
- Modify as findings justify: `.github/ISSUE_TEMPLATE/bug_report.yml`
- Modify as findings justify: `CONTRIBUTING.md`
- Modify as findings justify: `NOTICE.md`
- Modify as findings justify: `docs/GITHUB_LISTING.md`
- Modify as findings justify: `docs/PUBLISHING_CHECKLIST.md`
- Modify as findings justify: `docs/RELEASE_NOTES_2.0.0.md`
- Modify as findings justify: `docs/REVERSE_ENGINEERING_REPORT.md`
- Modify as findings justify: `docs/TEST_REPORT_2.0.0.md`
- Modify as findings justify: `docs/TROUBLESHOOTING.md`
- Modify as findings justify: `source-kit/PATCH_SOURCE_NOTICES.md`
- Modify as findings justify: `source-kit/docs/BUILD_FROM_ORIGINAL.md`
- Modify as findings justify: `source-kit/docs/LICENSING.md`
- Modify as findings justify: `source-kit/docs/PATCH_MAP.md`

**Interfaces:**
- Consumes: existing technical claims and evidence boundaries.
- Produces: concise, idiomatic English that becomes the factual reference point for localized pages.

- [ ] **Step 1: Review titles, metadata, headings, CTAs, captions, FAQ and body copy**

Remove inflated phrases, awkward noun stacks, duplicated proof claims, bureaucratic wording, and unnecessary slogans while preserving every factual boundary.

- [ ] **Step 2: Review technical documentation paragraph by paragraph**

Prefer direct constructions such as “The final 2.0.0 APK passed…” over compressed phrases such as “exact release-signed APK verified and physically hardware accepted.” Do not simplify away evidence distinctions.

- [ ] **Step 3: Check list parallelism and terminology**

Use one stable vocabulary for release file/artifact, physical-camera test, connection/reconnection, live preview, downloads/exports, offline account, and verification.

- [ ] **Step 4: Commit the English editorial pass**

```bash
git commit -m "docs: humanize public English copy"
```

### Task 3: Edit the Polish website as native Polish

**Files:**
- Modify: `site/pl/index.html`
- Modify if generated Polish site CTA wording requires it: `.github/workflows/update-readme-download.yml`

**Interfaces:**
- Consumes: exact existing facts and site structure.
- Produces: natural Polish public copy with unchanged links/markers/JSON-LD structure.

- [ ] **Step 1: Normalize grammar and inflection**

Use idiomatic forms such as `dla Androida`, natural release/download wording, and ordinary support vocabulary. Avoid calques such as “kanoniczny plik” in user-facing copy.

- [ ] **Step 2: Rewrite stiff or slogan-like headings where needed**

Keep headings short, but make them sound like Polish UI/help copy rather than translated English taglines.

- [ ] **Step 3: Align metadata, JSON-LD FAQ, visible FAQ and accessibility text**

Equivalent claims should use consistent Polish terminology across visible and machine-readable text.

- [ ] **Step 4: Commit**

```bash
git commit -m "docs: polish Polish site copy"
```

### Task 4: Edit the Ukrainian website as native Ukrainian

**Files:**
- Modify: `site/uk/index.html`
- Modify if generated Ukrainian site CTA wording requires it: `.github/workflows/update-readme-download.yml`

**Interfaces:**
- Consumes: exact existing facts and structure.
- Produces: contemporary idiomatic Ukrainian without Russian-influenced or literal-English constructions.

- [ ] **Step 1: Normalize terminology, word order, and aspect**

Prefer natural support/product phrasing; remove literal constructions such as overly formal equivalents of “final signed APK” where a simpler phrase carries the same facts.

- [ ] **Step 2: Review headings, instructions, FAQ and metadata independently**

Do not force English sentence structure onto Ukrainian.

- [ ] **Step 3: Check punctuation, apostrophes, dash usage and list consistency**

- [ ] **Step 4: Commit**

```bash
git commit -m "docs: refine Ukrainian site copy"
```

### Task 5: Edit the German website as idiomatic German

**Files:**
- Modify: `site/de/index.html`
- Modify if generated German site CTA wording requires it: `.github/workflows/update-readme-download.yml`

**Interfaces:**
- Consumes: exact existing facts and structure.
- Produces: concise German technical/support copy without translated-English syntax or needless passive voice.

- [ ] **Step 1: Replace calques and bureaucratic compounds**

Prefer natural German UI/support wording. Keep product/technical names unchanged.

- [ ] **Step 2: Normalize address and tone**

Keep the page consistently practical and readable; avoid mixing stiff formal prose with conversational imperatives.

- [ ] **Step 3: Review CTA grammar, metadata, FAQ and accessibility text**

- [ ] **Step 4: Commit**

```bash
git commit -m "docs: refine German site copy"
```

### Task 6: Edit the Russian website as native Russian

**Files:**
- Modify: `site/ru/index.html`
- Modify if generated Russian site CTA wording requires it: `.github/workflows/update-readme-download.yml`

**Interfaces:**
- Consumes: exact existing facts and structure.
- Produces: natural Russian technical/support prose with unnecessary English removed.

- [ ] **Step 1: Remove gratuitous English and literal translations**

Use Russian equivalents for live preview, Mi account, European region, release/support wording, and ordinary UI concepts when no precision is lost. Preserve genuine names such as APK, Android, HyperOS, GitHub, RTSP, ARM64, hashes, packages, and model codes.

- [ ] **Step 2: Normalize technical phrasing and sentence rhythm**

Prefer ordinary Russian support language over bureaucratic constructions.

- [ ] **Step 3: Confirm language selector invariants**

Russian stays last and text-only; no Russian flag is introduced.

- [ ] **Step 4: Commit**

```bash
git commit -m "docs: refine Russian site copy"
```

### Task 7: Synchronize GitHub-facing current copy without touching READMEs

**Files/objects:**
- Review/update: repository About description if the wording materially improves without changing claims
- Review/update: Issue #1
- Review/update: GitHub Release `v2.0.0` body to remain aligned with edited `docs/RELEASE_NOTES_2.0.0.md`
- Modify as needed: `.github/workflows/update-readme-download.yml`

**Interfaces:**
- Consumes: edited repository text.
- Produces: consistent public GitHub copy and future generated CTAs.

- [ ] **Step 1: Review Issue #1 as support copy**

Keep the compatibility-feedback purpose and privacy warning, but remove unnecessary formality or repetition.

- [ ] **Step 2: Review repository About description**

Keep it compact enough for GitHub and factually bounded. Do not imply continuous Android 8.1–16 testing where 10–11 are untested.

- [ ] **Step 3: Keep release body synchronized with the edited release-notes document**

Do not alter the release asset, tag, digest, signing information, or release status.

- [ ] **Step 4: Verify release-sync generator wording**

Only change generated site CTA labels if the current label is unnatural. README mutation logic remains intact and no README content is changed in this branch.

### Task 8: Run the second editorial pass and validation gates

**Files:**
- Read/validate: every changed file
- Do not modify READMEs

**Interfaces:**
- Consumes: all editorial edits.
- Produces: verified branch ready for PR.

- [ ] **Step 1: Prove README immutability**

Compare `main...language/full-editorial-pass-2026-09-11` and fail if any changed path has basename `README.md` or matches `README.*.md`.

Expected: zero README files changed.

- [ ] **Step 2: Run permanent repository validators**

```bash
python tools/verify_public_naming.py
python tools/verify_repository_integrity.py
```

Expected: both exit 0.

- [ ] **Step 3: Parse all five locale pages and JSON-LD**

Verify HTML language, canonical/hreflang, JSON-LD validity, social metadata, local media references, expected language order, and Russian text-only selector.

- [ ] **Step 4: Run terminology/factual-drift scans**

Check changed localized pages for known translation residue and check all changed files for accidental changes to hashes, model identifiers, package/version values, Android 10/11 status, OTA caveat, or release URLs.

- [ ] **Step 5: Browser-check representative widths**

At minimum test all five locales at one narrow mobile viewport and one desktop viewport, including navigation, CTA wrapping, trust strip, headings, FAQ, and download panel. Expand viewport coverage if any language is close to overflow.

- [ ] **Step 6: Perform a manual second read**

Read every changed public text file from top to bottom after the first edits. Correct remaining repetition, inconsistent terminology, unnatural punctuation, or overly dense sentences.

- [ ] **Step 7: Create a reviewable PR**

PR description must state:

```text
- README files unchanged
- technical/release claims unchanged
- languages reviewed: EN / PL / UK / DE / RU
- public docs and GitHub-facing copy reviewed
- validators/browser checks passed
```

Do not merge until the final diff confirms the constraints above.
