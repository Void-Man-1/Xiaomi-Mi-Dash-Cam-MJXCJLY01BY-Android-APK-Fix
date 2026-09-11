# Full Language Editorial Pass — Design

## Purpose

Run a repository-wide editorial quality pass over public-facing prose so the project reads like it was written by competent humans in each language rather than translated mechanically. The pass must improve grammar, syntax, idiom, rhythm, readability, terminology, punctuation, formatting, and tone without changing technical facts or product claims.

## Hard constraints

- **Do not modify any README file.** This includes `README.md` and every localized `README.*.md` file.
- Do not modify the published `v2.0.0` APK, release asset, checksum, signing identity, package name, version metadata, model identifiers, URLs, evidence files, test results, or technical semantics.
- Do not add marketing claims, broaden compatibility claims, or weaken caveats.
- Preserve established technical terms where translation would be misleading: APK, Android, HyperOS, Wi-Fi, SHA-256, RTSP, ARM64, ARMv7, GitHub, package names, model codes, and code identifiers.
- Russian remains the last language in the selector and remains text-only without a Russian flag image.

## Scope

### Website

Review all five public locale pages:

- `site/index.html` — English
- `site/pl/index.html` — Polish
- `site/uk/index.html` — Ukrainian
- `site/de/index.html` — German
- `site/ru/index.html` — Russian

The review includes visible copy and public metadata: titles, descriptions, Open Graph/Twitter copy, JSON-LD descriptions and FAQ text, navigation labels, hero copy, buttons, status labels, feature descriptions, installation instructions, verification captions, FAQ questions/answers, footer text, alt text, and accessibility labels.

### Public non-README repository text

Review user-facing prose in non-README Markdown/YAML/text surfaces, including where applicable:

- `.github/ISSUE_TEMPLATE/bug_report.yml`
- `CONTRIBUTING.md`
- `NOTICE.md`
- `docs/AUDIT_2026-09-11.md`
- `docs/GITHUB_LISTING.md`
- `docs/PUBLISHING_CHECKLIST.md`
- `docs/RELEASE_NOTES_2.0.0.md`
- `docs/REVERSE_ENGINEERING_REPORT.md`
- `docs/TEST_REPORT_2.0.0.md`
- `docs/TROUBLESHOOTING.md`
- other non-README public documentation discovered during the inventory
- public evidence notes outside README-named files when they contain user-facing prose

Historical audit/design/plan documents should only be edited if they contain current user-facing instructions or statements that would materially mislead a reader. Do not rewrite historical records merely for style.

### GitHub-facing copy

Review:

- repository About/description text;
- open Issue #1 wording;
- issue-template labels/descriptions/prompts;
- release notes for the current release;
- wording produced by `.github/workflows/update-readme-download.yml` when it writes localized website/release strings.

README-targeting behavior of the release-sync workflow must remain functionally intact, but README file contents are not to be edited in this pass.

## Editorial standard

Each language is edited independently as native prose, not as a word-for-word translation of English.

### English

Use concise, direct technical English. Remove needless repetition, inflated wording, bureaucratic phrasing, and slogan-like fragments where they obscure meaning. Prefer ordinary product/support language over formal report language on public-facing pages.

### Polish

Use natural Polish inflection and idiom. Avoid English-derived noun stacks, literal calques, unnecessary technical bureaucratese, and unnatural forms such as `APK dla Android` where `APK dla Androida` is appropriate. Use familiar Polish UI/support terminology while preserving technical names.

### Ukrainian

Use natural contemporary Ukrainian, not Russian-influenced or literal English syntax. Prefer idiomatic technical/support vocabulary and normal sentence order. Remove constructions that read like machine translation while preserving all factual boundaries.

### German

Use idiomatic German technical/support prose. Avoid English sentence structure transplanted into German, excessive passive voice, noun-heavy bureaucratic constructions, and unnatural phrases such as literal equivalents of “final signed APK.” Buttons and headings must read naturally as German UI copy.

### Russian

Use natural Russian technical/support prose. Avoid unnecessary English insertions such as `live preview`, `Mi Account`, or `EU / European region` when an established Russian equivalent is clearer. Keep genuine product names and technical identifiers unchanged. Avoid bureaucratic or overly formal phrasing.

## Tone

The project should sound competent, practical, and restrained. It should not sound like advertising copy, a legal filing, a machine translation, or an overexcited engineering log.

Use:

- short-to-medium sentences;
- concrete verbs;
- clear cause/effect relationships;
- normal native-language UI wording;
- precise caveats where evidence is limited.

Avoid:

- excessive slogans;
- stacked adjectives;
- redundant restatements of the same proof;
- inflated terms such as “canonical” when “published release file” is clearer;
- gratuitous English in localized prose;
- literal translation artifacts;
- overuse of passive voice;
- sentence fragments unless they are appropriate UI labels.

## Formatting pass

After prose editing, check each affected surface for:

- heading capitalization and hierarchy;
- consistent punctuation and dash style;
- spacing around version numbers, model codes, and technical terms;
- list parallelism;
- consistent terminology for camera, app, live preview, download/export, accountless/offline behavior, release, and verification;
- CTA/button grammar;
- paragraph density and repeated wording;
- localized metadata length/readability;
- accessible alt/ARIA wording.

Do not change layout/CSS unless revised text exposes a real overflow or readability defect. If that occurs, make the smallest layout adjustment needed and verify all five locales.

## Fact-preservation rule

Every edited sentence must remain equivalent in factual scope to the current repository evidence. In particular:

- `v2.0.0` remains the immutable current release;
- physical-camera acceptance is limited to the documented setup and features;
- Android 10 and 11 are not promoted to tested status;
- firmware OTA remains outside the completed acceptance claim;
- `MJXCJLY01BY` is the supported target and `MJXCJLY02BY` is not claimed compatible;
- no statement may imply Xiaomi endorsement or official status.

## Validation

The final branch must pass:

1. repository integrity/public naming validators;
2. a no-README-diff check proving every README file is byte-for-byte unchanged from `main`;
3. HTML/structured-data checks for all five locale pages;
4. browser checks at representative mobile and desktop widths to catch text overflow or broken layout after editing;
5. terminology scans for known machine-translation residues and forbidden factual drift;
6. a manual second editorial pass over every changed public text file.

The final review should report what was changed by language and call out any text deliberately left unchanged because it was already natural or because changing it risked altering technical meaning.
