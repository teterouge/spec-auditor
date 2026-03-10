# Audit Criteria Reference

Full taxonomy of issue types for each of the five audit passes, with examples and classification guidance.

---

## Table of Contents
1. [Pass 1: Completeness Issues](#pass-1-completeness-issues)
2. [Pass 2: Testability Issues](#pass-2-testability-issues)
3. [Pass 3: Ambiguity Issues](#pass-3-ambiguity-issues)
4. [Pass 4: Assumption Issues](#pass-4-assumption-issues)
5. [Pass 5: Scope Creep Issues](#pass-5-scope-creep-issues)
6. [Cross-Pass Patterns](#cross-pass-patterns)

---

## Pass 1: Completeness Issues

### Problem Statement

**What a good problem statement includes:**
- The user or actor experiencing the problem
- The specific situation or context in which the problem occurs
- The impact of the problem (what the user can't do, or does inefficiently)
- Evidence of the problem's existence (research, support tickets, data)

**Common failure modes:**

| Failure | Example | Why It's a Problem |
|---------|---------|-------------------|
| Solution masquerading as problem | "We need a dashboard for metrics" | Skips the question of why a dashboard is the right solution |
| Problem stated at wrong altitude | "Users can't manage their accounts" | Too broad — which part of account management? |
| Internal problem, not user problem | "We need to reduce engineering toil around X" | Valid, but different spec template needed |
| Assumed problem | "Users want faster search" | Is this validated? By what evidence? |

**Blocker threshold:** No problem statement at all, or a problem statement that is entirely a solution restatement.

---

### Success Metrics

**What good metrics look like:**
- Tied directly to the problem statement
- Specific and measurable (not "improve user satisfaction")
- Include a baseline and a target
- Have a defined measurement window
- Distinguish leading indicators from lagging outcomes

**Common failure modes:**

| Failure | Example | Classification |
|---------|---------|----------------|
| Vanity metric | "Increase page views" | 🟡 Warning — likely unmoved by the feature |
| Unmeasurable | "Users feel more confident" | 🔴 Blocker if this is the only metric |
| Missing baseline | "Improve conversion rate by 10%" | 🟡 Warning — 10% of what? |
| Metric disconnect | Problem is churn, metric is engagement | 🟡 Warning — may not validate the hypothesis |
| No measurement plan | Metric defined but no instrumentation noted | 🔵 Note |

---

### Out-of-Scope Definition

This is the most commonly missing field and one of the most valuable. Without it, scope creep is nearly inevitable.

**What a good out-of-scope section does:**
- Explicitly names things a reader might reasonably expect to be included
- Names things that *will* be built later but are not part of this version
- Names things that were considered and rejected (with brief rationale)

**Blocker threshold:** No out-of-scope definition when the feature has obvious adjacent scope that an engineer might reasonably implement.

---

### Error States

**Categories of error states to check for:**
- Network/connectivity errors
- Timeout errors
- Validation errors (user input)
- Authorization errors (user lacks permission)
- Not-found errors (resource doesn't exist)
- Conflict errors (concurrent edits, duplicate creation)
- Downstream service failures
- Rate limit errors
- Data integrity errors

**Blocker threshold:** Zero error states defined for any feature that touches external data, user input, or authentication.

---

## Pass 2: Testability Issues

### The Testability Standard

An AC is testable if and only if:
1. A QA engineer can write a test case without asking the PM a single question
2. Two different QA engineers would write functionally equivalent test cases
3. The test has a deterministic pass/fail outcome

### Vague Quality Descriptors — Full List

These words almost always produce untestable ACs. Flag every instance:

**Performance:** fast, quickly, responsive, snappy, smooth, instantaneous, real-time (without definition), near-real-time (without definition), minimal latency

**Usability:** intuitive, easy to use, simple, clear, obvious, user-friendly, accessible (without WCAG level specified), discoverable

**Quality:** good, appropriate, proper, correct, accurate (without threshold), complete, comprehensive, robust, reliable (without SLA)

**Aesthetics:** clean, polished, modern, consistent (without reference)

**Quantity:** several, many, few, some, various, numerous, adequate, sufficient

### Rewrite Patterns by Descriptor Type

**Performance descriptors → add specific thresholds with conditions:**
- "loads quickly" → "renders within [Xms] under [condition] on [platform]"
- "real-time" → "updates within [X] seconds of the triggering event"

**Usability descriptors → specify behavior, not feeling:**
- "easy to use" → "user can complete [task] without referring to documentation, measured by [usability test criteria]"
- "intuitive" → remove entirely and replace with the specific behavior you want

**Accuracy descriptors → add threshold and measurement method:**
- "accurate results" → "returns correct results for [X]% of test cases in [test dataset]"

**Consistency descriptors → reference the standard:**
- "consistent with the rest of the product" → "follows the design system specification in [link], specifically [component name] behavior"

---

## Pass 3: Ambiguity Issues

### Pronoun Drift

Pronouns become dangerous when multiple actors, systems, or objects are present in the same section. Flag every pronoun and verify its referent is unambiguous.

**High-risk contexts:**
- Specs with multiple user types (admin, end user, guest)
- Specs with multiple systems (frontend, backend, external API)
- Specs that reference both "the user" and "the system" acting on the same object

**Detection method:** Read each sentence containing a pronoun in isolation. If it's ambiguous who or what the pronoun refers to, flag it.

---

### Undefined Terms

Product teams develop internal vocabulary that never gets defined. Common offenders:

- Product-specific feature names used without definition ("the widget," "the pipeline," "the flow")
- Role names that have fuzzy definitions ("admin," "power user," "team member")
- States that have specific meaning in the product context ("active," "pending," "verified")
- Technical terms used loosely ("cache," "sync," "refresh," "update")

**Rule:** Any term that a new engineer joining the team would need to ask about should be defined or linked to a definition.

---

### Implicit Conditional Logic

Conditional logic that's written as a statement rather than a condition. The "if" is implicit.

**Examples:**
- "Show the upgrade prompt" → *when?* This is a conditional with no condition.
- "Users with permissions can edit" → *which permissions?* Defined where?
- "Admins see additional options" → *which options?* Always? Or only in certain states?

**Detection:** Read every "can," "should," "will," "may," and "must" statement and ask: *under what conditions?*

---

### Conflicting Requirements

Two ACs that cannot both be true simultaneously, or that would require contradictory implementations.

**Common conflict patterns:**
- AC says field is required; another AC describes behavior when field is empty
- AC says action is immediate; another AC says action requires confirmation
- AC defines a default state; another AC defines behavior that contradicts that default

**Detection:** After reading all ACs, mentally simulate a user walking through the feature. Where do you hit a fork that the spec doesn't resolve?

---

## Pass 4: Assumption Issues

### System Behavior Assumptions

These are assumptions about how existing systems work that may not be true, may not be documented, or may be about to change.

**Detection questions:**
- Does this feature assume the API returns data in a specific format?
- Does this feature assume a specific authentication state?
- Does this feature assume a specific database schema or data model?
- Does this feature assume a specific service is available or has specific SLA?

**Classification:** Mark as "confirm" if the assumption is likely true but unverified. Mark as "document" if true but not written down. Mark as "validate" if there's genuine uncertainty.

---

### Data Availability Assumptions

**What to check:**
- Is the data this feature needs already being collected?
- Is it accessible from the service that will serve it?
- Is it in the format the feature expects?
- At the volume and latency the feature requires?

**High-risk signals in spec language:**
- "Pull from the existing data"
- "Use the user's [X]" — where X is a field that may or may not exist
- "Show historical [X]" — how far back? Is that data retained?

---

### Permission and Role Assumptions

**For every role-differentiated behavior, check:**
- Is the role system fully defined?
- Is this behavior defined for every role, or just some?
- What happens when a user has multiple roles or partial permissions?
- Is the permission model already built, or is this spec depending on work that doesn't exist yet?

---

## Pass 5: Scope Creep Issues

### The Minimum/Maximum Interpretation Test

For any potentially unbounded requirement, perform this test:
1. **Minimum interpretation:** What is the smallest amount of work that technically satisfies this requirement?
2. **Maximum interpretation:** What is the most expansive amount of work that could be justified by this requirement?
3. **Gap assessment:** If the gap between minimum and maximum is more than a day of engineering work, the requirement needs to be bounded.

### High-Risk Phrases — Full List

Flag every instance of these phrases and apply the min/max test:

| Phrase | Typical Min | Typical Max | Bounding Strategy |
|--------|-------------|-------------|-------------------|
| "handle all edge cases" | Handle 0 unlisted cases | Handle every theoretically possible input | List the specific edge cases explicitly |
| "support future extensibility" | No action | Full plugin architecture | Define the specific extension points, if any |
| "integrate with existing system" | Read one field from one endpoint | Full bidirectional sync | Define the specific data contract |
| "work across all platforms" | Current platform only | Every OS/device/browser | List the supported platforms explicitly |
| "follow best practices" | Minimal compliance | Exhaustive adherence | Reference the specific standard or document |
| "be consistent with the rest of the product" | Visual similarity | Full behavioral parity | Reference the specific pattern to follow |
| "include appropriate error handling" | No handling | Handle every possible error | List the specific error states to handle |
| "support all user types" | Current user types | All hypothetical future user types | List the specific user types explicitly |
| "make it easy to add X later" | Document a note | Build the full architecture | Define what "easy" means technically |
| "handle large amounts of data" | Handle current data volumes | Handle infinite scale | Define the specific volume threshold |

---

## Cross-Pass Patterns

### The "Looks Good at a Glance" Spec

These specs have all the sections filled in but fail multiple passes on close inspection. Common characteristics:
- Generic metrics that don't tie to the problem
- ACs that are complete sentences but untestable
- No out-of-scope section
- Dependencies listed but not detailed

These specs are often more dangerous than obviously incomplete specs because they pass a superficial review.

### The "Too Early" Spec

A spec submitted before the problem is validated. Characteristics:
- Problem statement references internal need rather than user problem
- No evidence cited for the problem
- Success metrics are output metrics (shipped the feature) rather than outcome metrics
- No user research referenced

Flag this pattern explicitly in the sprint readiness verdict.

### The "Copy-Forward" Spec

A spec that was templated from a previous feature without proper adaptation. Characteristics:
- Generic language that could apply to any feature
- Success metrics copied from a different feature type
- Out-of-scope section that references things that don't apply to this feature
- ACs that are templated examples, not actual requirements

These almost always contain Pass 3 and Pass 4 findings.
