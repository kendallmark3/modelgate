# Intent: sort imports
Outcome: imports in every Python file under src/ are sorted in the project's standard order.
Inputs: the src/ tree and the existing isort configuration in pyproject.toml.
Outputs: the same files with reordered imports.
Success criteria: `isort --check src/` exits 0.
Constraints: no other changes.
