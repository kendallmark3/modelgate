# Intent: refund flow
Outcome: support agents can issue partial refunds through the payment provider.
Inputs: orders service, payments service, the provider's refund API, the ledger tables.
Outputs: a refund endpoint, ledger entries that reconcile, and an audit log entry per refund.
Success criteria: refunds never exceed the captured amount, including under concurrent requests; ledger balances reconcile.
Constraints: money movement; must be idempotent; no double refunds.
