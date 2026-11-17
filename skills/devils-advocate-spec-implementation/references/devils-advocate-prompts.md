# Devil's Advocate Prompts & Templates

## 1. Design Fork Adversarial Prompt (Fresh-Context Subagent)

Pass **only** the `PROPOSAL` and `SPEC CONTRACT` (strip your persuasive reasoning):

```text
Act as a skeptical Devil's Advocate reviewer. Your sole job is to find flaws,
blind spots, and spec violations in this proposal. Assume the author is
overconfident. Do NOT validate or praise.

Attack along these vectors:
1. Unstated assumptions not guaranteed by the spec or runtime.
2. Edge cases & failure modes (null/empty, malformed input, concurrency, partial failure, idempotency).
3. Spec drift: anything missing from SPEC CONTRACT OR unrequested complexity/scope creep.
4. Coupling & reversibility: hidden state, tight dependencies, hard-to-reverse choices.
5. Simpler alternative: is there a cleaner design that still satisfies 100% of SPEC CONTRACT?

Output numbered findings with severity (BLOCKER / MAJOR / MINOR) and concrete failure scenarios, or state explicitly that no flaws were found after checking all 5 vectors.

PROPOSAL:
<paste 3-5 sentence proposal + interface/code snippet>

SPEC CONTRACT:
<paste relevant SPEC-REQ-* items and constraints>
```

## 2. Post-Implementation Spec-Drift Audit Prompt

```text
Adversarial spec-compliance audit. Compare the DIFF against the SPEC CONTRACT.
Look specifically for:
- Spec requirements partially implemented, skipped, or subtly altered
- Unrequested behavior, flags, abstractions, or dead code ("gold-plating")
- Weakened tests, skipped assertions, or silent exception swallowing
- Edge cases mentioned in the spec that lack test coverage

Report ONLY concrete discrepancies with file:line references, or state "NO SPEC DRIFT FOUND".

SPEC CONTRACT:
<paste SPEC-REQ-* table>

DIFF / CHANGED FILES:
<paste git diff or file ranges>
```

## 3. Decision Log Template

```markdown
### Decision Log
| ID | Decision | Spec Reqs | Devil's Advocate Challenge | Resolution | Rejected Alternatives |
|---|---|---|---|---|---|
| D-1 | ... | SPEC-REQ-1,2 | Raised risk of X on partial failure | Added idempotency key / rollback | In-memory cache (lost on restart) |
```

## 4. Spec Traceability Matrix Template

```markdown
### Spec Traceability Matrix
| Spec ID | Requirement Summary | Implementation (`file:symbol`) | Verification Evidence (Observed) | Status |
|---|---|---|---|---|
| SPEC-REQ-1 | ... | `path/to/file.py:func` | `pytest tests/test_x.py` (4 passed) | VERIFIED |
```
