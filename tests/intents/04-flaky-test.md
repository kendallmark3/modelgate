# Intent: fix the flaky checkout test
Outcome: `checkout.spec.ts` passes reliably in CI.
Inputs: the test, the checkout service, and CI logs showing it fails about one run in ten with a timeout.
Outputs: a fix for the underlying cause, not a longer timeout or a retry.
Success criteria: 50 consecutive CI runs pass.
Constraints: the cause is unknown; it may be in the test, the service, or shared test fixtures.
