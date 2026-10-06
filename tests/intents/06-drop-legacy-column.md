# Intent: drop the legacy `ssn_plain` column
Outcome: the unencrypted `ssn_plain` column no longer exists in the production users table.
Inputs: the users table and one migration file.
Outputs: a single migration that drops the column.
Success criteria: the column is gone; the application, which already reads only `ssn_encrypted`, is unaffected.
Constraints: irreversible in production; compliance requirement.
