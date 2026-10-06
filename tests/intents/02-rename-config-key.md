# Intent: rename config key
Outcome: the config key `timeout_ms` is called `timeoutMs` everywhere.
Inputs: src/config.ts and its two call sites.
Outputs: the same behavior with the renamed key.
Success criteria: existing tests pass.
Constraints: no behavior change.
