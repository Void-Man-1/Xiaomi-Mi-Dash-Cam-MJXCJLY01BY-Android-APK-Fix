# Full Repository Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Audit the repository end-to-end, fix only confirmed defects, and preserve the published `v2.0.0` APK byte-for-byte.

**Architecture:** Work on `audit/full-repository-2026-09-11`. Establish a baseline, add narrowly scoped regression checks before each fix, execute repository/security/source-kit/workflow/site checks, correct confirmed faults, and finish with one reviewable PR. Temporary audit-only workflow files may be used but must be removed before merge unless they provide durable regression value.

**Tech Stack:** GitHub Actions, PowerShell 5.1/7, Python 3, Android SDK build-tools (`aapt`, `zipalign`, `apksigner`), Apktool 3.0.3, HTML/CSS/JavaScript, Google Chrome/Playwright where needed, GitHub REST/CLI.

**Spec:** `docs/superpowers/specs/2026-09-11-full-repository-audit-design.md`

## Global Constraints

- Published `v2.0.0` APK is immutable.
- Published APK SHA-256 must remain `2F189C0D3A6C9965036EDDBFA927EB7FD720C47D611991EB5EC1D1055E89B887`.
- Do not re-sign, replace, retag, or silently mutate release `v2.0.0`.
- A critical defect in the release requires a new version/advisory, not replacement of `v2.0.0`.
- Fix only reproducible defects; avoid speculative refactors.
- Russian remains last in site language selectors and has no flag.
- Temporary audit scaffolding must be removed before final PR unless intentionally retained as regression protection.

---

### Task 1: Freeze the release baseline and repository inventory

**Files:**
- Read: `checksums/SHA256SUMS.txt`
- Read: `source-kit/checksums/original-apk.sha256`
- Read: `source-kit/patches/2.0.0/manifest.json`
- Read: `docs/RELEASE_NOTES_2.0.0.md`
- Create: `docs/AUDIT_2026-09-11.md`

**Interfaces:**
- Consumes: current `main`, latest release metadata, recursive repository tree.
- Produces: immutable baseline values and an audit findings ledger used by all later tasks.

- [ ] **Step 1: Record immutable release identity**

Capture release tag, asset name, asset size, release digest, package name, versionCode/versionName, and signing-certificate digest from existing repository/release metadata into `docs/AUDIT_2026-09-11.md`.

- [ ] **Step 2: Verify baseline consistency**

Run/compare:

```text
release asset: Mi-Dash-Cam-2.0.0.apk
release digest: sha256:2f189c0d3a6c9965036eddbfa927eb7fd720c47d611991eb5ec1d1055e89b887
repo checksum:  2F189C0D3A6C9965036EDDBFA927EB7FD720C47D611991EB5EC1D1055E89B887
```

Expected: all values agree exactly, case-insensitive for hex.

- [ ] **Step 3: Inventory repository state**

Record all tracked files, active branches, open PRs/issues, workflows, release assets, and Pages deployment state. Flag stale branches, orphan docs, duplicate binaries, and files not referenced anywhere.

- [ ] **Step 4: Commit the audit ledger skeleton**

```bash
git add docs/AUDIT_2026-09-11.md
git commit -m "docs: establish repository audit baseline"
```

### Task 2: Add durable repository-integrity regression checks

**Files:**
- Modify: `tools/verify_public_naming.py`
- Create: `tools/verify_repository_integrity.py`
- Modify: `.github/workflows/verify-public-naming.yml`

**Interfaces:**
- Consumes: repository tree, release/checksum metadata, site/docs text.
- Produces: one command that fails on stale release state, broken localized navigation, wrong social-preview metadata, missing files, inconsistent checksums, or forbidden Russian flag rendering.

- [ ] **Step 1: Write failing checks for known defects**

Add tests/checks that currently fail when:

```text
- issue/docs still describe v2.0.0 as a release candidate
- og:image/twitter:image point to the portrait app screenshot
- any locale omits one of en/pl/uk/de/ru navigation entries
- Russian has an image/flag
- checksum text disagrees with the immutable release digest
- referenced local site media does not exist in the deployed artifact source set
```

- [ ] **Step 2: Run the checks and confirm failure**

```bash
python tools/verify_repository_integrity.py
python tools/verify_public_naming.py
```

Expected: failure on the social-preview condition before the preview fix is applied.

- [ ] **Step 3: Wire the check into CI**

Update `.github/workflows/verify-public-naming.yml` to run both validators with read-only contents permission.

- [ ] **Step 4: Re-run and retain only checks that encode stable project requirements**

Expected: known defects still fail; unrelated repository state passes.

- [ ] **Step 5: Commit**

```bash
git add tools/verify_public_naming.py tools/verify_repository_integrity.py .github/workflows/verify-public-naming.yml
git commit -m "test: add repository integrity regression checks"
```

### Task 3: Audit source-kit safety and reproducibility

**Files:**
- Read/modify as findings require: `source-kit/scripts/Common.ps1`
- Read/modify as findings require: `source-kit/scripts/prepare-original.ps1`
- Read/modify as findings require: `source-kit/scripts/apply-patches.ps1`
- Read/modify as findings require: `source-kit/scripts/build.ps1`
- Read/modify as findings require: `source-kit/scripts/verify.ps1`
- Read/modify as findings require: `source-kit/patches/2.0.0/manifest.json`
- Create only if justified: `.github/workflows/verify-source-kit.yml`

**Interfaces:**
- Consumes: pinned original APK checksum, patch manifest, vendored patch payloads, Android build tools.
- Produces: verified or corrected deterministic patch/build/verification pipeline.

- [ ] **Step 1: Parse all PowerShell scripts without executing mutations**

Use PowerShell parser APIs on Windows and PowerShell 7:

```powershell
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($path,[ref]$null,[ref]$errors) | Out-Null
if ($errors.Count) { throw ($errors | Out-String) }
```

Expected: zero syntax errors for all five scripts.

- [ ] **Step 2: Exercise path-containment and archive-safety helpers with hostile fixtures**

Create temporary fixtures containing `../`, rooted paths, duplicate ZIP entries, symlink/reparse-point edge cases where supported, and paths outside `source-kit/work`/`source-kit/build`. Expected: helpers reject escape attempts and never delete outside allowed generated roots.

- [ ] **Step 3: Validate manifest integrity**

Check that every `fileChanges`, `addedFiles`, `deletedFiles`, and `vendorInputs` entry points to a valid repository payload where applicable; hashes are well-formed SHA-256 values; required vendor inputs are pinned; and `apktoolVersion` is exact.

- [ ] **Step 4: Exercise apply/build/verify failure modes**

Test controlled cases for wrong original checksum, wrong vendor checksum, missing required vendor input, wrong Apktool version, unsigned build, missing ABI, malformed ELF, bad ZIP alignment, and signing key located inside the repository.

Expected: each case fails closed with a specific error.

- [ ] **Step 5: Attempt an unsigned full reconstruction if all required vendor inputs are available**

```powershell
./scripts/prepare-original.ps1 ...
./scripts/apply-patches.ps1
./scripts/build.ps1 -ApktoolPath <3.0.3>
./scripts/verify.ps1 -ApkPath ./build/Mi-Dash-Cam-2.0.0-unsigned.apk
```

Expected: deterministic patched-file hashes and successful static verification. The output must be clearly named unsigned/local and must not equal or replace the published signed release artifact.

- [ ] **Step 6: Fix only reproduced source-kit defects, adding regression fixtures first**

For each confirmed defect, add the smallest failing fixture/check, verify failure, implement minimal fix, and re-run the relevant source-kit tests.

- [ ] **Step 7: Commit source-kit fixes separately**

```bash
git add source-kit .github/workflows/verify-source-kit.yml
git commit -m "fix: harden source-kit reproducibility checks"
```

Skip this commit if no source-kit code changes are needed.

### Task 4: Audit GitHub Actions and automation behavior

**Files:**
- Modify as findings require: `.github/workflows/deploy-pages.yml`
- Modify as findings require: `.github/workflows/update-readme-download.yml`
- Modify as findings require: `.github/workflows/verify-public-naming.yml`

**Interfaces:**
- Consumes: release events, pushes to `main`, Pages source tree.
- Produces: least-privilege, non-recursive, fail-closed automation.

- [ ] **Step 1: Validate YAML and action references**

Parse every workflow, confirm referenced action versions exist, and flag unnecessary write permissions or mutable/unpinned references where correction has concrete value.

- [ ] **Step 2: Test release-sync logic against controlled release metadata**

Simulate at least:

```text
v2.0.0 + correct Mi-Dash-Cam-2.0.0.apk -> updates nothing
v2.1.0 + correct Mi-Dash-Cam-2.1.0.apk -> updates all 5 site locales + 4 localized READMEs + root README
v2.1.0 + missing canonical asset -> hard failure, no partial edits
```

Expected: idempotent output and no stale localized CTA grammar.

- [ ] **Step 3: Check workflow recursion and branch/path filters**

Ensure release-sync commits do not recursively trigger themselves indefinitely, Pages deploy runs when site/media actually changes, and validation runs on relevant PR/push paths.

- [ ] **Step 4: Check shell quoting and permissions**

Confirm untrusted filenames/metadata cannot become shell syntax and each job has the minimum token scope needed.

- [ ] **Step 5: Fix confirmed automation defects and rerun controlled cases**

Expected: all three release-sync scenarios plus workflow syntax checks pass.

- [ ] **Step 6: Commit**

```bash
git add .github/workflows
git commit -m "fix: harden repository automation"
```

Skip if no workflow changes are needed.

### Task 5: Correct stale documentation and repository-facing state

**Files:**
- Modify as findings require: `README.md`
- Modify as findings require: `docs/README.pl.md`
- Modify as findings require: `docs/README.uk.md`
- Modify as findings require: `docs/README.de.md`
- Modify as findings require: `docs/README.ru.md`
- Modify as findings require: `docs/GITHUB_LISTING.md`
- Modify as findings require: `docs/PUBLISHING_CHECKLIST.md`
- Modify as findings require: `docs/TEST_REPORT_2.0.0.md`
- Modify as findings require: `docs/RELEASE_NOTES_2.0.0.md`
- Modify: GitHub issue #1

**Interfaces:**
- Consumes: immutable release facts and physical-test evidence.
- Produces: public claims that match the actual final release state.

- [ ] **Step 1: Cross-check all version/test/model claims**

Search for `release candidate`, `pending`, `remaining release gate`, stale filenames, old repository URLs, `MJXCJLY02BY` mislabeling, and claims that blur physical-camera evidence with emulator/device-only testing.

- [ ] **Step 2: Confirm the stale issue fails the new integrity check**

Issue #1 currently says the remaining release gate is real-camera testing. Record that as a Medium finding.

- [ ] **Step 3: Update issue #1 to the final-release state**

Replace release-candidate wording with concise current status: 2.0.0 is final, physical-camera acceptance completed on Poco F6/Android 16, and the thread remains for compatibility feedback. Preserve the warning not to post credentials/private data.

- [ ] **Step 4: Fix any additional stale docs found**

Make the smallest wording/link corrections needed; do not rewrite correct technical documentation for style alone.

- [ ] **Step 5: Run documentation/link validators**

```bash
python tools/verify_repository_integrity.py
python tools/verify_public_naming.py
```

Expected: all documentation/model/release-state checks pass except the still-pending social-card test until Task 6.

- [ ] **Step 6: Commit repository documentation fixes**

```bash
git add README.md docs
git commit -m "docs: align public state with final 2.0.0 release"
```

### Task 6: Replace the broken social preview and audit all Pages locales

**Files:**
- Create: `site/social-preview.png`
- Modify: `site/index.html`
- Modify: `site/pl/index.html`
- Modify: `site/uk/index.html`
- Modify: `site/de/index.html`
- Modify: `site/ru/index.html`
- Modify as findings require: `site/styles.css`
- Modify as findings require: `site/app.js`
- Modify as findings require: `.github/workflows/deploy-pages.yml`

**Interfaces:**
- Consumes: existing app icon, product identity, site design language.
- Produces: 1200×630 social card and validated five-locale Pages output.

- [ ] **Step 1: Generate the dedicated social card**

Required visual content:

```text
Mi Dash Cam
MJXCJLY01BY
Android compatibility fix
Android 8.1 / 9 / 12–16 · HyperOS
```

Use the project/app icon and a restrained device/app visual. Do not use flags or dense body text. Output exactly `1200×630` PNG.

- [ ] **Step 2: Add a failing metadata test before changing HTML**

The validator must require every locale's `og:image` and `twitter:image` to reference the canonical Pages-hosted `social-preview.png`, and require `og:image:width=1200`, `og:image:height=630` where added.

- [ ] **Step 3: Update all locale metadata**

Use a stable Pages URL, not `raw.githubusercontent.com`:

```text
https://void-man-1.github.io/Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix/social-preview.png
```

- [ ] **Step 4: Run static HTML/metadata validation**

Check canonical/hreflang reciprocity, sitemap entries, JSON-LD parseability, duplicate IDs, missing local assets, language order, Russian text-only selector, and localized title/description presence.

- [ ] **Step 5: Run real-browser geometry/media smoke tests on all five locales**

Viewport matrix:

```text
360×800
390×844
768×1024
1024×900
1366×900
1440×1000
```

For each locale, assert:

```text
scrollWidth == clientWidth
language row has no hidden horizontal scroll
release/trust strip remains centered
4 SVG flags load; Russian has no flag
embedded MP4 element is present
poster loads
screenshot cards are not cropped by CSS
no console errors from local JS/assets
```

- [ ] **Step 6: Fix only reproduced Pages defects and rerun the matrix**

Expected: 30/30 locale/viewport cases pass.

- [ ] **Step 7: Commit**

```bash
git add site .github/workflows/deploy-pages.yml tools/verify_repository_integrity.py
git commit -m "fix: improve Pages metadata and social preview"
```

### Task 7: Security and repository-hygiene sweep

**Files:**
- Modify only confirmed findings.
- Update: `docs/AUDIT_2026-09-11.md`

**Interfaces:**
- Consumes: full tracked tree and generated audit artifacts.
- Produces: documented security/hygiene result with false positives resolved.

- [ ] **Step 1: Scan tracked content for secret/key indicators**

Search for private-key headers, keystore extensions, tokens, passwords, authorization headers, cloud credentials, APK signing secrets, and accidentally committed local paths.

Expected: no real secret material. Known checksum/certificate fingerprints are not secrets and must be classified correctly.

- [ ] **Step 2: Scan for suspicious executable/download behavior**

Inspect PowerShell and workflows for `Invoke-Expression`, unsafe `Start-Process` argument composition, unquoted shell interpolation, unpinned remote binary downloads, destructive recursive deletes without containment checks, and archive extraction without traversal protection.

- [ ] **Step 3: Review branch/repository hygiene**

Identify stale superseded audit/fix branches and open PRs. Do not delete anything tied to active work. Record cleanup recommendations separately from product fixes.

- [ ] **Step 4: Fix only confirmed security/hygiene defects**

For each code defect, add a regression check first, demonstrate failure, patch minimally, then re-run the affected check.

- [ ] **Step 5: Record finding severity and disposition**

For every finding in `docs/AUDIT_2026-09-11.md`, record:

```text
ID | severity | evidence | affected files | fix | regression check | status
```

- [ ] **Step 6: Commit**

```bash
git add docs/AUDIT_2026-09-11.md <confirmed-fix-files>
git commit -m "audit: document security and repository findings"
```

### Task 8: Final verification, cleanup, review, and PR

**Files:**
- Modify: `docs/AUDIT_2026-09-11.md`
- Delete: any temporary audit-only workflow/fixture not intentionally retained.

**Interfaces:**
- Consumes: all prior task outputs.
- Produces: clean final branch ready for merge.

- [ ] **Step 1: Re-verify immutable release state**

Re-fetch latest release and assert:

```text
tag == v2.0.0
asset == Mi-Dash-Cam-2.0.0.apk
sha256 == 2F189C0D3A6C9965036EDDBFA927EB7FD720C47D611991EB5EC1D1055E89B887
```

Expected: unchanged from Task 1.

- [ ] **Step 2: Run every durable validator and CI job**

Expected: repository integrity, public naming, source-kit checks, workflow tests, and Pages/browser checks all pass.

- [ ] **Step 3: Remove temporary scaffolding**

Delete one-shot workflows, downloaded audit fixtures, temporary generated APKs, and test-only assets that are not deliberate regression tests.

- [ ] **Step 4: Review the full diff against `main`**

Confirm no release asset/tag mutation, no signing-key material, no unrelated reverse-engineering changes, no accidental binary duplication, and no cosmetic churn outside confirmed findings.

- [ ] **Step 5: Finalize the audit report**

Summarize Critical/High/Medium/Low findings, fixes applied, checks executed, known limitations, and any items intentionally deferred because they require a new release or unavailable hardware.

- [ ] **Step 6: Commit final cleanup/report**

```bash
git add -A
git commit -m "audit: finalize repository verification report"
```

Skip if there is no final diff.

- [ ] **Step 7: Open one PR**

PR title:

```text
audit: harden repository quality, reproducibility and public metadata
```

PR body must state explicitly that `v2.0.0` and its published SHA-256 were not changed, list findings by severity, and include the exact verification matrix/results.

- [ ] **Step 8: Merge only after all required checks pass**

Use squash merge unless preserving multiple commits provides clear review value. After merge, verify the production Pages deployment and the deployed `social-preview.png` URL, then clean stale audit branches if safe.
