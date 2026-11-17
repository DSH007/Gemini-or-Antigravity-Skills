---
name: devils-advocate-spec-implementation
description: Implements an approved plan or specification strictly to the spec while enforcing Devil's Advocate decision-making at every non-trivial design, assumption, or implementation choice. Use when the user asks to implement a plan with devil's advocate decision making, enforce strict to-the-spec implementation, challenge assumptions during coding, or prevent spec drift and over-engineering.
---

# Devil's Advocate & To-the-Spec Implementation

Execute an approved plan or specification with zero silent spec drift and adversarial scrutiny at every non-trivial decision point.

## When to Use

- Implementing a formal spec, PRD, ADR, or improvement plan where correctness and contract fidelity matter
- User explicitly asks for Devil's Advocate decision-making and to-the-spec implementation
- High-risk changes involving state transitions, public interfaces, concurrency, security, migrations, or multi-module boundaries

**When NOT to use:** Trivial one-line edits or exploratory throwaway prototypes where no spec exists yet (create a spec first with `spec-driven-development`).

## Non-Negotiable Rules

1. **Spec is the contract**: Implement every specified requirement (`SPEC-REQ-*`). Do not silently omit edge cases, weaken checks, or invent unrequested features ("gold-plating").
2. **Challenge before committing**: Every non-trivial decision must survive a Devil's Advocate attack before code is locked in.
3. **Escalation over guessing**: If a spec requirement is ambiguous or contradictory, stop and clarify with the user rather than silently picking an interpretation.

## Workflow

### Phase 1: Spec Lock & Requirement Extraction

Before writing code:
1. Read the full plan/specification and referenced code files.
2. Extract an explicit **Spec Traceability Checklist**:
   - Assign stable IDs (`SPEC-REQ-1`, `SPEC-REQ-2`, ...) for every functional requirement, interface contract, constraint, error behavior, and out-of-scope boundary.
3. Surface any ambiguity, contradiction, or missing error case immediately. Resolve before coding.

### Phase 2: Devil's Advocate Decision Gate (For Every Non-Trivial Choice)

Trigger this gate whenever a task involves branching design choices, interface contracts, shared state/concurrency, external I/O, security boundaries, or irreversible operations:

1. **State the Proposal + Contract**: Write in 3–5 sentences *what* you propose to build and *which* `SPEC-REQ-*` constraints it must satisfy.
2. **Run the Devil's Advocate Challenge**:
   - **Preferred (fresh context)**: Invoke a fresh-context subagent (`research` or `code-reviewer`) using the adversarial prompt in [references/devils-advocate-prompts.md](./references/devils-advocate-prompts.md). Pass ONLY the proposal + spec contract (never your rationale for why you like it).
   - **Fallback (if nested/subagent unavailable)**: Explicitly adopt a hostile Devil's Advocate stance in a separate block attacking your own proposal and flag it as self-challenged.
3. **Attack Vectors to Cover**:
   - Hidden assumptions not guaranteed by the spec or types
   - Unhandled edge cases (empty/null/huge/malformed inputs, retries, partial failures)
   - Ordering, race conditions, or state-corruption risks
   - Spec drift (does this add unrequested behavior or miss a subtle spec clause?)
   - Simpler alternative that satisfies the spec with less coupling
4. **Reconcile & Log**:
   - Accept valid critiques (revise design), or rebut with concrete code/spec evidence.
   - Record a concise entry in the **Decision Log** (Decision, Alternatives Rejected, Why Accepted).

### Phase 3: To-Spec Incremental Implementation

1. Implement one vertical `SPEC-REQ-*` slice at a time.
2. Write or run tests proving both the **happy path** and **adversarial/boundary cases** surfaced in Phase 2.
3. Keep diffs focused strictly on the active `SPEC-REQ-*` items—no unrelated refactors.

### Phase 4: Spec Compliance & Adversarial Diff Audit

Before reporting completion:
1. **Traceability Audit**: Map every `SPEC-REQ-*` to exact file paths, symbol names, and observed verification evidence (tests, typecheck, lint, runtime output). Every item must be `VERIFIED` (never `ASSUMED`).
2. **Final Devil's Advocate Diff Review**: Challenge the final diff using the post-implementation audit prompt in [references/devils-advocate-prompts.md](./references/devils-advocate-prompts.md) to catch subtle spec drift, dead code, or weakened assertions.
3. Report the **Spec Traceability Table**, **Decision Log**, and exact observed test/check results.
