# spec-auditor

An adversarial spec review plugin for Claude Code. Audits product specs, PRDs, and feature briefs across five passes before they reach engineering — surfacing blockers, untestable acceptance criteria, ambiguities, hidden assumptions, and scope creep risks.

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

```bash
# Add this repo as a marketplace
/plugin marketplace add <your-github-username>/spec-auditor

# Install the plugin
/plugin install spec-auditor@pm-discipline
```

Or manually:
```bash
git clone <repo-url>
claude --plugin-dir ./spec-auditor
```

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

## Structure

```
spec-auditor/
├── .claude-plugin/
│   ├── plugin.json          ← Plugin manifest
│   └── marketplace.json     ← Marketplace catalog
├── skills/
│   └── spec-auditor/
│       ├── SKILL.md         ← Core audit instructions
│       ├── references/
│       │   ├── audit-criteria.md
│       │   ├── acceptance-criteria-patterns.md
│       │   └── severity-guide.md
│       ├── scripts/
│       │   └── spec_parser.py
│       └── evals/
│           └── evals.json
└── README.md
```

---

## Design Notes

**Adversarial, not collaborative.** Calibrated to find problems, not validate the work. A spec that passes all five passes clean has earned that verdict.

**Severity avoids over-flagging.** Not everything is a blocker. High-risk features (payments, auth, irreversible actions) have a lower escalation threshold.

**Rewrites, not just flags.** Pass 2 and Pass 5 model what fixed looks like — original and rewrite side by side.

---

## Part of the pm-discipline Suite

- **spec-auditor** ← you are here
- **feature-roi-forecaster** — Financial business case before the spec is written
- **post-launch-retro** — Closes the loop between hypotheses and reality
- **pmf-signal-analyzer** — Multi-signal product-market fit assessment
- **dependency-risk-mapper** — Cross-team dependency graph and delivery risk
- **competitive-intel-synthesizer** — Competitive signals to roadmap implications
- **pricing-packaging-intel** — Pricing and packaging recommendation engine
- **stakeholder-comm-translator** — Audience-specific message translation