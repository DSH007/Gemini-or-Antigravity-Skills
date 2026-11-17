# Improvement Plan Template

```markdown
# Improvement Plan: [System / Initiative Name]

## 1. Objective & Scope
- **Goal:** [Concise outcome]
- **In Scope:** [Modules, endpoints, pipelines]
- **Out of Scope:** [Explicit exclusions]
- **Constraints:** [Compatibility, budget, latency SLA, hardware]

## 2. Baseline, Targets & Guardrails

### Primary Metrics (Success Criteria)
| Metric | Measurement Command / Method | Baseline (Observed) | Target | Phase Due |
|---|---|---|---|---|
| e.g., Query latency (p95) | `python benchmark.py --queries 50` | `2.40s` | `<= 1.20s` (-50%) | Phase 2 |

### Guardrail Metrics (Must Not Regress)
| Guardrail | Measurement Command / Method | Baseline (Observed) | Allowed Bound |
|---|---|---|---|
| e.g., Eval pass rate / F1 | `python evaluate.py` | `0.86` | `>= 0.85` (max -0.01) |
| e.g., Unit test suite | `pytest` | `100% pass` | `100% pass` |

**Measurement Conditions:** [Dataset/fixture, sample size N, machine/env, git SHA]

## 3. Bottleneck Diagnosis (Evidence)
1. **[Bottleneck Name]** (`file.py:L10-L45`): [Observed evidence — profiler breakdown, error distribution, trace].
2. **[Bottleneck Name]** (...): [...]

## 4. Prioritized Initiatives

| ID | Initiative | Target Bottleneck | Expected Delta | Effort / Risk | Rollback Trigger |
|---|---|---|---|---|---|
| I-1 | ... | Bottleneck 1 | -600ms p95 | Low / Low | Any eval drop > 1% |
| I-2 | ... | Bottleneck 2 | -400ms p95 | Med / Med | Memory > 2GB |

## 5. Phased Execution & Metric Gates

### Phase 0: Measurement Harness (if any baseline is UNMEASURED)
- [ ] Implement deterministic benchmark/eval command and record baselines.

### Phase 1: [Quick Wins / Foundation]
- [ ] Task 1.1 (I-1): [Files + exact change]
- **Gate 1:** Re-run measurement commands; confirm target progress and zero guardrail breaches.

### Phase 2: [Core Structural Improvements]
- [ ] Task 2.1 (I-2): [Files + exact change]
- **Gate 2:** Full benchmark + regression suite passes target & guardrails.

## 6. Post-Implementation Verification Protocol
- Run A/B or before/after comparison on identical fixture/commit range.
- Record final observed metrics table alongside baseline before closing.
```
