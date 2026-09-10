# Full Repository Audit Design

## Goal

Perform a repository-wide quality, security, reproducibility, documentation, automation, and website audit for `Xiaomi-Mi-Dash-Cam-MJXCJLY01BY-Android-APK-Fix`, fix only confirmed defects, and leave the published `v2.0.0` release artifact immutable.

## Immutable release constraint

The published `v2.0.0` APK is immutable. The audit must not replace, rebuild in place, re-sign, retag, or otherwise alter the published `Mi-Dash-Cam-2.0.0.apk` asset. Its published SHA-256 remains authoritative:

`2F189C0D3A6C9965036EDDBFA927EB7FD720C47D611991EB5EC1D1055E89B887`

If the audit discovers a critical security defect in the published APK, the remedy is a new release with a new version number and explicit advisory; the existing `v2.0.0` artifact remains unchanged.

## Audit method

Work from an isolated audit branch. Establish evidence before making each fix. A finding is actionable only when it is reproducible from repository state, workflow behavior, release metadata, rendered site behavior, or static analysis. Avoid speculative refactors.

Temporary audit workflows, scripts, or fixtures may be used to execute checks that cannot be run through the GitHub connector alone. Temporary scaffolding must be removed before the final PR unless it provides durable regression protection.

Every confirmed fault should have a regression check when practical. Final changes should be grouped into coherent commits and submitted through one reviewable PR rather than a sequence of direct `main` edits.

## Audit domains

### 1. Repository structure and hygiene

Inspect the recursive tree, branch state, ignored/generated content, duplicate or stale files, obsolete helper artifacts, naming consistency, broken relative references, orphaned documentation, unnecessary binary duplication, and repository metadata that no longer matches the shipped project.

Stale development branches may be removed only when they are already merged/superseded and are not required by an open PR or documented workflow.

### 2. Release integrity and reproducibility

Verify the current GitHub release identity, asset name, digest, package/version claims, checksum files, release notes, documentation links, and source-kit manifest references.

Audit `source-kit` for deterministic patch application, safe path handling, checksum enforcement, vendor-input pinning, expected deletion/addition checks, APK tool/version pinning, alignment verification, signing behavior, and failure modes. Reproduction checks may build unsigned or locally test-signed artifacts, but they must never overwrite or masquerade as the immutable `v2.0.0` release.

### 3. Security

Search repository content and generated artifacts for committed secrets, private-key material, credentials, tokens, unsafe archive/path traversal handling, command-injection opportunities, untrusted path expansion, accidental signing-key inclusion, insecure workflow permissions, mutable third-party action references where risk justifies correction, and overly broad GitHub token privileges.

Distinguish between security properties of the repository/build system and properties of Xiaomi's legacy application. Do not broaden the audit into unrelated reverse-engineering changes unless a repository defect depends on them.

### 4. GitHub Actions and automation

Audit all workflows for trigger correctness, least privilege, concurrency, branch/path filters, release-event behavior, recursion/self-trigger risk, shell quoting, failure propagation, action versions, artifact handling, Pages deployment correctness, and release-link synchronization.

Exercise workflows where practical on the audit branch or through temporary validation jobs. A passing YAML parse is not sufficient; important logic should be executed against controlled inputs.

### 5. Documentation and public claims

Cross-check `README.md`, localized READMEs, release notes, test reports, reverse-engineering documentation, troubleshooting guidance, evidence notes, publishing checklist, issue templates, repository description/topics, and open issues against the current final `v2.0.0` state.

Claims must distinguish physical-camera evidence, emulator/device-only evidence, static verification, and untested functionality. Model naming must consistently distinguish `MJXCJLY01BY` from `MJXCJLY02BY` / Mi Dash Cam 1S.

Localized public copy should remain natural and technically equivalent across English, Polish, Ukrainian, German, and Russian. Russian remains last in site language selectors and has no flag.

### 6. Website and social metadata

Audit all five GitHub Pages locales for HTML validity, canonical and `hreflang` relationships, sitemap/robots consistency, JSON-LD validity, release metadata, links, accessibility, responsive geometry, language selector behavior, media loading, video fallback behavior, reduced-motion handling, and stale or untranslated strings.

Run real-browser checks at representative mobile, tablet, laptop, and desktop widths. Detect horizontal overflow, clipped controls, missing media, broken flags, duplicate IDs, inaccessible controls, and incorrect language order.

Replace the current Open Graph/Twitter preview source, which uses a raw portrait app screenshot, with a dedicated 1200×630 project social card. The visual should communicate `Mi Dash Cam`, `MJXCJLY01BY`, Android compatibility, and the project purpose immediately. The image should be served from the Pages site or another stable same-project URL and referenced consistently by all locale metadata.

### 7. Issues and repository-facing UX

Review open issues/templates and repository-facing guidance for stale release-state claims. Confirm issue #1 no longer describes `v2.0.0` as a release candidate or says real-camera acceptance is still pending, because the final release and evidence now document completed hardware acceptance.

## Severity model

- **Critical:** exposed secret/signing material, release-integrity compromise, code execution or path traversal in normal contributor workflows, or a defect requiring a security advisory/new release.
- **High:** build/reproduction logic can silently produce an incorrect artifact; release/download metadata can point at the wrong artifact; deployment or automation can corrupt public state.
- **Medium:** broken documented workflow, stale public claim that materially misleads users, inaccessible/broken site function, or a meaningful localization/metadata defect.
- **Low:** hygiene, presentation, dead references, minor wording, or maintainability issues with concrete user/contributor impact.

Critical and high findings are fixed first. Medium findings are fixed when reproducible. Low findings are fixed when the change is low-risk and clearly improves the project; cosmetic churn without evidence is excluded.

## Testing and acceptance

The final PR is acceptable only when:

1. The immutable release asset and published SHA-256 are unchanged.
2. Repository-wide static checks and secret/key scans pass.
3. Source-kit scripts parse and their safety/integrity checks pass against controlled audit fixtures; a full reconstruction is attempted when required inputs/tooling are available.
4. GitHub Actions syntax and executed workflow logic pass.
5. Public naming/release-link synchronization checks pass.
6. All five Pages locales pass browser geometry, navigation, metadata, media, and accessibility smoke checks.
7. The new social preview image is 1200×630, referenced by `og:image` and `twitter:image`, and retrievable from the deployed site after merge.
8. Stale public documentation/issues found by the audit are corrected.
9. Temporary audit-only scaffolding is removed unless intentionally retained as a regression test.
10. The final PR diff is reviewed for unrelated changes before merge.

## Known findings at design time

Two confirmed defects already exist:

1. `og:image` and `twitter:image` currently use `assets/screenshots/poco-f6-v2.0.0-main.png`, a portrait in-app screenshot that produces a poor and ambiguous social preview.
2. Open issue #1 still describes `v2.0.0` as a release candidate and says real-camera acceptance remains outstanding, contradicting the published final release notes and hardware evidence.

These are audit findings, not assumptions, and will be corrected during implementation.
