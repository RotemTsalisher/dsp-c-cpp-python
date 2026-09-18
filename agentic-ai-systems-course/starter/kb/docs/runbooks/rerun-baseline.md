# Runbook: re-record a baseline

Use this when a deliberate change makes the stored baseline invalid - a new
firmware release, a tolerance change, or a fixture replacement. Do **not** use it
to make a failing run pass; a baseline re-record hides regressions by definition.

## Before you start

1. Confirm the change is deliberate and recorded. A baseline re-record requires
   an ADR if it is caused by a tolerance or convention change.
2. Confirm the rig is the one the family's baseline was originally recorded on.
   Cross-rig baselines are not comparable; fixture geometry differs.
3. Note the current baseline run id. You will need it to roll back.

       python -m bench baselines show --family DUT-7X

## Procedure

1. Warm the rig for 20 minutes. The first measurement of a cold session is
   systematically different and must not become a baseline.

2. Run the full sweep three times:

       python -m bench run --family DUT-7X --firmware 4.2 --graph full --repeat 3

3. Check inter-run spread. Any metric varying by more than 20% of its tolerance
   across the three runs means the rig is unstable. Stop and fix the rig; a
   baseline recorded on an unstable rig produces months of false regressions.

4. Select the **median** run per metric, not the best one. Choosing the best run
   biases every future comparison and guarantees a false regression rate.

       python -m bench baselines propose --from-runs R-1 R-2 R-3 --strategy median

5. Review the diff against the outgoing baseline. Every metric that moved by more
   than its tolerance needs an explanation before you promote.

       python -m bench baselines diff --family DUT-7X --against current

6. Promote, recording the reason:

       python -m bench baselines promote --run R-2 --reason "firmware 4.2 release"

7. Re-run the nightly comparison manually to confirm it is green against the new
   baseline before leaving it to the scheduler.

## Rollback

       python -m bench baselines promote --run <previous-run-id> --reason "rollback"

Baselines are immutable runs, so rollback is a pointer change and takes seconds.
Stored comparisons that referenced the interim baseline are invalidated and will
be recomputed on next access.

## After

- Note the new baseline run id and the reason in the family's change log.
- If the baseline changed because of a tolerance or convention change, link the ADR.
- Expect the first nightly after promotion to show small diffs on unrelated
  metrics. That is the median-selection effect, not a regression.
