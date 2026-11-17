---
name: improvement-plan-with-metrics
description: Creates an evidence-backed engineering or system improvement plan anchored on reproducible baseline metrics, falsifiable target metrics, non-regression guardrail metrics, and prioritized initiatives. Use when the user asks to create an "improvement plan with metrics", optimize latency/accuracy/cost/quality/reliability, define KPIs/benchmarks before refactoring, or build a measurable roadmap.
---

# Improvement Plan with Metrics

Build an actionable improvement plan grounded in measured baselines, explicit targets, non-regression guardrails, and falsifiable verification gates—never vague "make it faster/better" goals.

## When to Use

- Planning performance, accuracy, reliability, developer-experience, or cost improvements
- User asks for an "improvement plan with metrics", optimization roadmap, or benchmark-driven refactoring plan
- Existing benchmarks or quality scores exist (or need to be established) before changing code

**When NOT to use:** One-off bug fixes with an obvious root cause (use `debugging-and-error-recovery`), or pure greenfield feature specs (use `spec-driven-development`).

## Core Principles

1. **No baseline, no plan**: Every target metric must have a measured baseline (or an explicit Phase 0 task to measure it before any optimization code is written).
2. **Every primary metric needs a guardrail**: Optimizing one metric in isolation hides regressions (e.g., latency improves because accuracy or error handling broke). Pair every primary target with explicit guardrails.
3. **Attribution per initiative**: Each proposed change must state *which* bottleneck it addresses, *why* (evidence), its *expected metric delta*, and its *rollback trigger*.

## Workflow

### Step 1: Frame Objective & Scope

1. Define the system boundary, workload/dataset, and constraints (cost, backward compatibility, SLA, hardware).
2. Identify 1–3 **Primary Metrics** (what we want to move) and 2–4 **Guardrail Metrics** (what must not regress).

### Step 2: Capture Reproducible Baselines

1. Run existing benchmarks, evaluations, profilers, or test suites—or write a minimal reproducible benchmark command if none exists.
2. Record for every metric:
   - Exact measurement command
   - Environment / dataset / sample size (`N`, hardware, model/config)
   - Current baseline value (e.g., p50, p95, throughput, pass rate, coverage, bundle KB, memory MB)
   - Variance / noise floor if applicable

Never fabricate or extrapolate numbers. Mark unmeasured metrics explicitly as `UNMEASURED (Phase 0 measurement required)`.

### Step 3: Diagnose Bottlenecks With Evidence

Profile or inspect logs/traces/evals to pinpoint where time, errors, or quality loss actually come from (e.g., I/O wait, N+1 calls, chunking/retrieval recall drop, cold start, lock contention). Link each bottleneck to observed evidence (file paths, profiler output, failure cases).

### Step 4: Set Targets, Guardrails & Prioritize Initiatives

1. Define **Target Metrics** (numeric threshold + deadline/phase) and **Guardrail Thresholds** (hard fail bounds).
2. Propose concrete initiatives ranked by **Impact × Confidence / Effort**:
   - Hypothesis & mechanism
   - Expected metric delta (range)
   - Risks & failure modes
   - Rollback / abort trigger
3. Order into phases with explicit **Metric Gates** (do not proceed to Phase N+1 if Phase N fails its gate or breaches a guardrail).

### Step 5: Write the Plan Document

Author the plan using [references/plan-template.md](./references/plan-template.md) (save to `IMPROVEMENT_PLAN.md`, `docs/improvement_plan.md`, or the session artifact directory as appropriate).

### Step 6: Validate Plan Completeness

Verify before presenting:
- [ ] Every metric has an exact runnable measurement command.
- [ ] Every baseline number is observed (or explicitly flagged `UNMEASURED` as Task 1).
- [ ] Guardrail metrics cover correctness/quality alongside speed/cost.
- [ ] Every phase ends with a pass/fail metric gate.
