# Uniform Project Naming Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Migrate the Mi Dash Cam project to one stable naming scheme across repository content, release asset metadata, website languages, and future build/release automation.

**Architecture:** Use a repository-wide validator as the migration contract, then update text/build naming on an isolated branch. Merge the verified content migration, rename the existing GitHub release asset in place and update the release metadata through a one-time Actions workflow, then perform the repository slug change as the single manual admin step and patch Pages URLs immediately afterward.

**Tech Stack:** GitHub repository/Actions/Releases/Pages, Markdown, static HTML, Python validation, PowerShell build scripts.

**Spec:** `docs/superpowers/specs/2026-09-10-uniform-project-naming-design.md`

## Global Constraints

- Repository target: `Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix`.
- Display title: `Xiaomi Mi Dash Cam MJXCJLY01BY Android APK Fix`.
- Release APK: `Mi-Dash-Cam-2.0.0.apk`; future pattern `Mi-Dash-Cam-<version>.apk`.
- `EU` may remain only where it is a technical compatibility fact, including `com.banyac.mijia.app.eu` and explicit European-variant support warnings.
- Never rebuild or resign the accepted 2.0.0 APK solely for naming; its SHA-256 remains `2F189C0D3A6C9965036EDDBFA927EB7FD720C47D611991EB5EC1D1055E89B887`.
- Do not break EN/RU/PL language navigation or Pages deployment.

---

### Task 1: Add naming migration validator

**Files:**
- Create: `tools/verify_public_naming.py`

**Interfaces:**
- Consumes: checked-out repository tree.
- Produces: exit code 0 only when canonical branding/file patterns and required page-language links are present; nonzero with precise violations otherwise.

- [ ] **Step 1: Add validator rules**

The script must verify the canonical display title, canonical APK stem/pattern, required EN/RU/PL page files and links, and reject known legacy public branding strings such as `Mi-Dash-Cam-EU-` and `Mi Dash Cam EU 2.0.0`. It must allow `com.banyac.mijia.app.eu` and compatibility prose containing `European`/`EU variant`.

- [ ] **Step 2: Run validator against current branch and verify RED**

Expected: nonzero because the current tree still contains legacy APK/release branding and source-kit output naming.

- [ ] **Step 3: Commit validator**

Commit message: `test: add public naming migration validator`.

### Task 2: Migrate repository content and build naming

**Files:**
- Modify: `README.md`
- Modify: `docs/GITHUB_LISTING.md`
- Modify: `docs/PUBLISHING_CHECKLIST.md`
- Modify: `docs/README.ru.md`
- Modify: `docs/README.pl.md`
- Modify: `docs/RELEASE_NOTES_2.0.0.md`
- Modify: `docs/TEST_REPORT_2.0.0.md` where public artifact names appear
- Modify: `docs/TROUBLESHOOTING.md` where project branding appears
- Modify: `release-assets/README.md`
- Modify: `checksums/SHA256SUMS.txt`
- Modify: `source-kit/scripts/build.ps1`
- Modify: `.github/workflows/update-readme-download.yml`
- Modify: `site/index.html`
- Modify: `site/ru/index.html`
- Modify: `site/pl/index.html`
- Modify: `site/robots.txt`
- Modify: `site/sitemap.xml`
- Remove temporary one-time language helper/workflow if still present after confirming their work is already represented in committed site files.

**Interfaces:**
- Consumes: canonical names from the spec.
- Produces: repository tree that references `Mi-Dash-Cam-2.0.0.apk`, uses the new public project title, preserves technical regional caveats, and emits future contributor build names based on `Mi-Dash-Cam-<version>`.

- [ ] **Step 1: Update user-facing branding and artifact references**

Replace public `EU` branding and old long APK filename with the canonical names while preserving technical compatibility statements.

- [ ] **Step 2: Harden release-sync asset selection**

Select the canonical asset for the current version by exact expected name `Mi-Dash-Cam-${version}.apk` rather than selecting the first `.apk` asset.

- [ ] **Step 3: Update source-kit output naming**

Change `$releaseName` from `Mi-Dash-Cam-EU-$version` to `Mi-Dash-Cam-$version`, retaining only state/signing suffixes.

- [ ] **Step 4: Run validator and verify GREEN**

Expected: exit 0 for public naming rules that are independent of the yet-unperformed repository slug rename.

- [ ] **Step 5: Review diff and commit**

Commit message: `refactor: standardize Mi Dash Cam project naming`.

### Task 3: Merge the content migration

**Files:** repository branch only; no new source files.

**Interfaces:**
- Consumes: verified migration branch.
- Produces: verified changes on `main` without yet changing the repository slug.

- [ ] **Step 1: Open PR from `migration/uniform-naming` to `main`**
- [ ] **Step 2: Inspect changed filenames and full diff**
- [ ] **Step 3: Re-run/inspect repository validation CI if available**
- [ ] **Step 4: Merge only after the diff matches the naming spec**

### Task 4: Rename release asset and release metadata in place

**Files:**
- Create temporarily on `main`: `.github/workflows/rename-release-asset-once.yml`
- Delete after successful execution.

**Interfaces:**
- Consumes: GitHub Release `v2.0.0`, asset ID `544212226` or dynamically resolved asset by digest/name.
- Produces: same binary asset under `Mi-Dash-Cam-2.0.0.apk`, release title `Mi Dash Cam 2.0.0`, release body synchronized to the canonical filename.

- [ ] **Step 1: Add one-time workflow**

The workflow resolves `v2.0.0`, verifies the existing asset digest is the accepted SHA-256, PATCHes the release asset name in place, updates release title/body, and does not upload or rebuild a binary.

- [ ] **Step 2: Run workflow**

Expected: success and asset name exactly `Mi-Dash-Cam-2.0.0.apk`.

- [ ] **Step 3: Fetch release and verify asset name, size, digest, title, and body**

Expected size: `30437934`; digest: `sha256:2f189c0d3a6c9965036eddbfa927eb7fd720c47d611991eb5ec1d1055e89b887`.

- [ ] **Step 4: Verify direct download endpoint and synchronized README/site references**
- [ ] **Step 5: Delete one-time workflow**

### Task 5: Manual repository rename boundary

**Files:** none.

**Interfaces:**
- Consumes: current repository with completed content/asset migration.
- Produces: repository slug `Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix`.

- [ ] **Step 1: Ask owner to rename repository in GitHub Settings → General**

This is the one required manual step because the connected GitHub App does not expose repository-administration mutation.

- [ ] **Step 2: Verify repository resolves under the new slug before proceeding**

### Task 6: Post-rename Pages/URL migration

**Files:**
- Modify: `README.md`
- Modify: `docs/GITHUB_LISTING.md`
- Modify: `site/index.html`
- Modify: `site/ru/index.html`
- Modify: `site/pl/index.html`
- Modify: `site/robots.txt`
- Modify: `site/sitemap.xml`
- Modify other text files containing hard-coded old repository URLs discovered by repository scan.

**Interfaces:**
- Consumes: renamed repository slug.
- Produces: all canonical, hreflang, Open Graph, structured-data, download/release, raw-image, and sitemap URLs aligned with the new GitHub and GitHub Pages paths.

- [ ] **Step 1: Replace hard-coded old repository slug with new slug**
- [ ] **Step 2: Run naming/URL validator**
- [ ] **Step 3: Commit URL migration**
- [ ] **Step 4: Verify Pages workflow success**
- [ ] **Step 5: Fetch live EN/RU/PL URLs, robots.txt, sitemap.xml, and APK CTA; verify HTTP success and correct canonical/hreflang metadata**

### Task 7: Final migration audit

**Files:** none.

**Interfaces:**
- Consumes: final repository/release/site state.
- Produces: evidence-backed completion report.

- [ ] **Step 1: Scan default branch for prohibited legacy branding and old repository slug**
- [ ] **Step 2: Fetch `v2.0.0` and verify asset digest/size/name**
- [ ] **Step 3: Verify repository title/about guidance file and EN/RU/PL site content**
- [ ] **Step 4: Verify no temporary migration workflow/helper remains**
- [ ] **Step 5: Report only verified results and any remaining manual GitHub metadata fields**
