# Severity Classification Guide

How to determine whether a finding is a 🔴 Blocker, 🟡 Warning, or 🔵 Note. Calibrated to avoid both over-flagging (everything is a blocker) and under-flagging (everything is a note).

---

## The Core Classification Question

For every finding, ask:

> **If engineering starts this sprint without resolving this issue, what is the expected outcome?**

| Expected Outcome | Severity |
|-----------------|----------|
| Engineering will make an assumption that is likely wrong, requiring rework | 🔴 Blocker |
| Engineering will make an assumption that *might* be wrong, creating mid-sprint confusion | 🟡 Warning |
| Engineering will make an assumption that is probably right, but the PM should confirm | 🔵 Note |

---

## 🔴 Blocker — Definition & Examples

**Definition:** A finding that, if unresolved, will cause one or more of:
- Engineering building the wrong thing (incorrect behavior)
- Engineering being blocked mid-sprint waiting for a PM decision
- QA being unable to verify the feature (no testable criteria exist)
- A feature that ships correctly against the spec but fails in production due to an unchecked assumption

**Automatic blockers (always 🔴):**
- No success metrics defined at all
- No acceptance criteria defined at all
- A required external dependency is not called out and ownership is unknown
- A spec that references a system behavior that engineering cannot verify without PM research
- Conflicting requirements that cannot both be implemented (one must be wrong)
- A critical user flow with zero error states defined

**Contextual blockers (🔴 based on feature risk):**

| Finding Type | Low-Risk Feature | High-Risk Feature |
|-------------|-----------------|-------------------|
| Missing out-of-scope definition | 🟡 Warning | 🔴 Blocker |
| Untestable primary success metric | 🟡 Warning | 🔴 Blocker |
| Undefined permission model | 🟡 Warning | 🔴 Blocker |
| Missing rollback/kill switch | 🔵 Note | 🔴 Blocker |
| Unconfirmed data availability assumption | 🟡 Warning | 🔴 Blocker |

**High-risk features** = any feature touching: payments, authentication, personal data, multi-tenancy, security controls, irreversible user actions, or external integrations.

---

### Blocker Examples

**Example 1 — Missing error state (high-risk feature)**
> The spec describes a payment flow but defines no behavior for payment failure, card decline, or network timeout.

Classification: 🔴 Blocker. Engineering will invent error handling. In payments, invented error handling is how money gets charged without confirmation or users get stuck.

---

**Example 2 — Conflicting requirements**
> AC #3 states "The form auto-saves every 30 seconds." AC #7 states "Changes are not persisted until the user clicks Save."

Classification: 🔴 Blocker. Both cannot be true. Engineering must stop and ask.

---

**Example 3 — Unverifiable dependency**
> "The feature pulls the user's purchase history from the orders API." — No endpoint, no data contract, no confirmation the orders API has this data.

Classification: 🔴 Blocker. Engineering cannot estimate or build without this. The sprint will be blocked the moment someone opens the orders API docs.

---

## 🟡 Warning — Definition & Examples

**Definition:** A finding that creates meaningful risk but won't necessarily stop the sprint. Engineering will probably make a reasonable assumption, but the PM should verify it's the *right* assumption before the sprint ends.

**Common warning patterns:**
- An AC that is testable but uses a loose threshold that needs PM confirmation ("within a few seconds" → PM should define the threshold)
- A missing out-of-scope definition for a low-risk feature
- An assumption that is likely true but unconfirmed
- A success metric that's directionally right but too vague for post-launch evaluation
- An edge case that's possible but infrequent, with no defined behavior

**Warning Examples**

**Example 1 — Loose threshold**
> "The search results load quickly"

Classification: 🟡 Warning (not 🔴 Blocker) because engineering will implement reasonable performance and the feature won't be broken — but the PM and engineering may have different definitions of "quickly" that surface in QA.

If the spec is for a high-traffic search feature where performance is a core value prop, escalate to 🔴 Blocker.

---

**Example 2 — Unconfirmed but likely assumption**
> The spec references "the user's billing address" without specifying where it comes from.

Classification: 🟡 Warning if billing address is almost certainly already collected and stored. Classification: 🔴 Blocker if there's any reason to doubt it exists.

---

**Example 3 — Missing edge case (low frequency)**
> A file upload feature with no defined behavior for duplicate file names.

Classification: 🟡 Warning. Engineering will handle this (probably with a rename or overwrite), but the PM should confirm which behavior is correct.

---

## 🔵 Note — Definition & Examples

**Definition:** A finding that is worth surfacing but won't affect the sprint outcome in most scenarios. These are polish items, documentation gaps, or nice-to-haves that the PM should address in a future revision.

**Common note patterns:**
- Missing instrumentation/analytics callouts (the feature should probably fire an event, but the absence won't break anything)
- Accessibility omissions on a non-primary user flow
- Copy/UX text not specified (engineering will use placeholder copy that can be revised)
- Missing link to design file (engineering can find it)
- Success metric defined but without a measurement window

**Note Examples**

**Example 1 — Missing event tracking callout**
> A new user action with no mention of analytics events to fire.

Classification: 🔵 Note. The feature ships either way. Engineering will probably ask, but they can work around it.

---

**Example 2 — Copy not specified**
> Error message behavior is defined ("display an error") but the exact copy is not.

Classification: 🔵 Note unless copy is a compliance or legal requirement.

---

## Calibration: Avoiding Over-Flagging

The most common calibration error is flagging everything as a blocker. This makes your audit report look like everything is on fire — and the PM stops trusting it.

**Gut-check questions before marking 🔴 Blocker:**
1. Would a senior engineer actually stop and ask the PM about this, or would they make a reasonable call and move on?
2. If engineering made the most obvious assumption here, would the feature be meaningfully wrong?
3. Is this actually a blocker, or am I covering myself by over-escalating?

**Gut-check questions before marking 🔵 Note:**
1. Could this cause a mid-sprint conversation that delays the sprint?
2. Is there a realistic scenario where the most common assumption is wrong?

If yes to either of these — it's probably a 🟡 Warning, not a Note.

---

## Severity by Finding Type — Quick Reference

| Finding Type | Default Severity | Escalate to 🔴 if... |
|-------------|-----------------|---------------------|
| Missing problem statement | 🔴 Blocker | Always |
| Missing success metrics | 🔴 Blocker | Always |
| No ACs defined | 🔴 Blocker | Always |
| Missing out-of-scope | 🟡 Warning | Feature has obvious adjacent scope |
| Untestable AC | 🟡 Warning | It's the primary or only AC |
| Vague quality descriptor | 🔵 Note | Feature's core value prop is that quality attribute |
| Undefined term | 🟡 Warning | Term is used in an AC or dependency |
| Pronoun ambiguity | 🟡 Warning | Pronoun could refer to a security-sensitive actor |
| Missing error state | 🟡 Warning | High-risk feature or irreversible action |
| Unconfirmed dependency | 🟡 Warning | Dependency is external or cross-team |
| Implicit conditional logic | 🟡 Warning | Condition is in an AC or affects a user-visible state |
| Scope creep risk phrase | 🟡 Warning | Gap between min/max interpretation is >2 days engineering work |
| Missing instrumentation | 🔵 Note | Feature is tied to a specific metric in the success criteria |
| Missing rollback plan | 🔵 Note | High-risk feature or affects many users |
| Copy not specified | 🔵 Note | Copy is legally or compliance-sensitive |
