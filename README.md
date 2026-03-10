# spec-auditor

An adversarial spec review skill for Claude Code. Audits product specs, PRDs, and feature briefs across five passes before they reach engineering — surfacing blockers, untestable acceptance criteria, ambiguities, hidden assumptions, and scope creep risks.

The goal is to catch everything a senior engineer or QA lead would raise in sprint planning, before sprint planning happens.

---

## Why This Exists

Most spec reviews are superficial. Someone reads it, says "looks good," and engineering picks it up. The problems surface mid-sprint: a missing error state, an untestable AC, a dependency nobody confirmed, a scope phrase that expands to three weeks of work.

This skill runs a structured adversarial audit — not a proofreading pass. It asks the questions nobody wants to hear until it's too late to ask them cheaply.

---

## What It Does

Five sequential audit passes, each targeting a different failure mode:

| Pass | What It Finds |
|------|--------------|
| 1. Completeness | Missing required fields — problem statement, success metrics, out-of-scope, error states, dependencies, rollback |
| 2. Testability | Acceptance criteria a QA engineer can't write a deterministic test for — rewrites each one |
| 3. Ambiguity | Language two engineers would interpret differently — pronoun drift, undefined terms, implicit conditionals, conflicting requirements |
| 4. Assumptions | Things the spec silently assumes — system behavior, data availability, permissions, platform, state/sequence |
| 5. Scope Risk | Unbounded requirements that will expand in implementation — flags each with min/max interpretation range and a bounded rewrite |

Every finding gets a severity rating:
- 🔴 **Blocker** — Sprint should not start without resolving this
- 🟡 **Warning** — Sprint can start but mid-sprint confusion is likely
- 🔵 **Note** — Worth addressing; won't block delivery

The output ends with a **Sprint Readiness Verdict**: Ready / Ready with fixes / Not ready.

---

## Installation

### Local Installation 

```bash
# Create the directory structure
mkdir -p ~/.claude/skills/spec-auditor/references
mkdir -p ~/.claude/skills/spec-auditor/scripts
mkdir -p ~/.claude/skills/spec-auditor/evals

# Place files
~/.claude/skills/spec-auditor/
├── SKILL.md
├── README.md
├── references/
│   ├── audit-criteria.md
│   ├── acceptance-criteria-patterns.md
│   └── severity-guide.md
├── scripts/
│   └── spec_parser.py
└── evals/
    └── evals.json
```

Restart Claude Code after installation. Verify with `/skills` — `spec-auditor` should appear in the list.

---

## Usage

The skill triggers automatically. Just share a spec and ask if it's ready:

```
"Can you review this PRD before I send it to engineering?"
"Is this spec ready to go into the sprint?"
"Take a look at these user stories and tell me what's missing."
"Quick gut check on this feature brief."
```

You can also upload a spec file directly. If a `.md`, `.txt`, `.html`, or `.docx` file is attached, the `spec_parser.py` script will extract structured elements before the audit begins.

---

## File Reference

| File | Purpose | When Claude reads it |
|------|---------|---------------------|
| `SKILL.md` | Core audit instructions and output template | Every audit |
| `references/audit-criteria.md` | Full issue taxonomy with examples for all five passes | When classifying ambiguous findings |
| `references/acceptance-criteria-patterns.md` | Good/bad AC examples by feature type (CRUD, search, auth, payments, etc.) | When rewriting untestable ACs in Pass 2 |
| `references/severity-guide.md` | Blocker vs. Warning vs. Note classification logic | When uncertain about severity |
| `scripts/spec_parser.py` | Extracts structured elements from uploaded spec files | When a file is attached |
| `evals/evals.json` | Test cases for benchmarking skill performance | Benchmarking only — not used at runtime |

---

## The spec_parser Script

Run directly for pre-processing or integration into other workflows:

```bash
# Human-readable output (default)
python scripts/spec_parser.py path/to/spec.md

# JSON output for machine processing
python scripts/spec_parser.py path/to/spec.md --format json

# One-line summary
python scripts/spec_parser.py path/to/spec.md --format summary
```

Supports: `.md`, `.txt`, `.html`, `.docx` (requires `python-docx` for docx; falls back gracefully if not installed).
Zero external dependencies for all other formats.

---

## Design Notes

**Adversarial, not collaborative.** The skill is calibrated to find problems, not validate the work. It will not soften findings because the spec looks mostly good. A spec that passes all five passes clean has earned that verdict.

**Severity is calibrated to avoid over-flagging.** Not everything is a blocker. The severity guide is specifically tuned so that the 🔴 rating retains credibility — if everything is a blocker, nothing is. High-risk features (payments, auth, irreversible actions) have a lower threshold for escalation.

**Rewrites, not just flags.** Pass 2 and Pass 5 don't just identify problems — they model what fixed looks like. The PM sees both the broken original and a working rewrite, side by side.

**Part of a larger PM skill set.** This skill is #1 in a suite of PM-discipline tools designed around the principle that the highest-leverage place to intervene is before engineering picks something up, not after.

---

## Related Skills

This skill pairs well with:
- **feature-roi-forecaster** — Builds the financial business case before the spec is written; if a feature can't justify its ROI, the spec shouldn't exist yet
- **dependency-risk-mapper** — Maps cross-team dependencies and delivery risk; complements the dependency section of this audit
- **post-launch-retro** — Closes the loop after launch; the hypotheses validated here become the baseline for retrospective analysis