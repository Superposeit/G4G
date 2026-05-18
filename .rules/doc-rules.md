---
title: Documentation Rules — G4G_Docs
date: 2026-04-17
tags:
  - meta
  - rules
aliases:
  - doc-rules
  - rules
---

# Documentation Rules — G4G_Docs

> [!important] These rules are mandatory for all contributors.
> Non-compliant files will be corrected before any version snapshot is taken.

---

## 1. Frontmatter (Required on Every File)

Every `.md` file must begin with YAML frontmatter:

```yaml
---
title: "Human-readable title"
date: YYYY-MM-DD          # date created or last significantly revised
version: X.Y.Z            # semver of this file (starts at 0.1.0)
tags:
  - category/subcategory  # at least one tag
status: draft | review | stable | frozen
---
```

**Status definitions:**

| Status | Meaning |
|---|---|
| `draft` | Work in progress — content incomplete or unreviewed |
| `review` | Complete but needs team validation before use |
| `stable` | Validated — safe to reference in submission materials |
| `frozen` | Archived version snapshot — do not edit |

---

## 2. Versioning Rules (Semver)

Files version independently from the repo tag.

| Change | Bump |
|---|---|
| Fix typo, reword sentence | PATCH `0.1.x` |
| Add new section or substantial content | MINOR `0.x.0` |
| Complete rewrite or structural overhaul | MAJOR `x.0.0` |

**Repo-level tags** (git tags) reflect the overall documentation milestone:
- `v0.x.0` — pre-submission iterations
- `v1.0.0` — submission-ready freeze
- Post-submission archives go into `versions/`

---

## 3. File Structure Rules

### Spec Documents (`docs/`)

- Numbered prefix `NN_` enforces reading order
- One document = one architectural concern
- Always link back to `[[main]]` where the topic appears in the master draft
- Max depth: H3 (`###`) — no H4 or deeper

### Research Notes (`research/papers/`)

- Format: `ACRONYM_kebab-title.md`
- Must include: citation block, abstract summary, EducaT relevance section
- Must be listed in `[[research/index]]`

### Versions (`versions/`)

- One directory per git tag: `versions/vX.Y.Z/`
- Contains `snapshot-notes.md` only — no full content copies
- Snapshot notes record: what changed, key decisions, open questions at that point
- **Frozen on creation — never edited after commit**

---

## 4. Writing Style Rules

- **Language:** English (technical, professional) for all docs
- **Voice:** Active, declarative. "EducaT uses INT4 quantization." Not "INT4 quantization is used."
- **Tense:** Present for design decisions ("the model runs locally"), past for meeting decisions ("the team decided to skip fine-tuning")
- **No vague hedging:** Avoid "might," "could potentially," "it is possible that"
- **Concrete over abstract:** Name the hardware (Snapdragon 680), the country (Dominican Republic), the curriculum (MINERD 2024)
- **No duplication:** If something is in `main.md`, reference it with a wikilink rather than copying it

---

## 5. Linking Rules

| Link type | Syntax | When to use |
|---|---|---|
| Internal note | `[[filename]]` | Always for files within this vault |
| Internal note + section | `[[filename#heading]]` | When linking to a specific section |
| External URL | `[display](https://url)` | Papers, competition pages, GitHub repos |
| Citation | See §6 below | Academic papers |

---

## 6. Citation Format

For academic papers referenced in `research/papers/`:

```
**Citation:** LastName, F. & LastName, M. (Year). *Title of Paper.*
Venue. https://doi.org/xxxxx · arXiv:XXXX.XXXXX
```

Papers must have a corresponding note in `research/papers/` before being
cited anywhere in `docs/` or `main.md`.

---

## 7. Diagram Rules

- All diagrams: Mermaid only (no external image dependencies)
- Every diagram must have a title comment on the first line: `%% Title %%`
- Keep diagrams self-contained — label nodes fully, don't rely on surrounding text to explain them
- Preferred diagram types: `graph TD`, `graph LR`, `sequenceDiagram`, `classDiagram`

---

## 8. Change Discipline

> [!warning] Every meaningful change requires a CHANGELOG entry.
> "Meaningful" = anything beyond fixing a typo or formatting.

Format for CHANGELOG entry:

```markdown
## [X.Y.Z] — YYYY-MM-DD
### Added | Changed | Fixed | Removed
- Description of change + rationale
```

---

## 9. Frozen File Protocol

Files in `versions/` are **immutable after initial commit.**

If you need to correct a frozen snapshot:
1. Add a `corrections.md` file in the same `versions/vX.Y.Z/` directory
2. Document the correction and date — do NOT edit the original snapshot
