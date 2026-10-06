"""Checks the ModelGate scorer over every input. Run: python3 -m unittest discover tests"""
import itertools
import json
import subprocess
import sys
import unittest
from pathlib import Path

SCORER = Path(__file__).resolve().parents[1] / "plugins/intent-driven-training/skills/model-gate/scripts/model-gate.py"
RANK = {"FAST": 0, "STANDARD": 1, "REASONING": 2}
FACTORS = ("complexity", "context", "consequence", "capability")


def run(scores, *extra):
    args = [sys.executable, str(SCORER)]
    for name, value in zip(FACTORS, scores):
        args += [f"--{name}", str(value)]
    return subprocess.run(args + list(extra), capture_output=True, text=True)


def tier(scores, *extra):
    return json.loads(run(scores, *extra).stdout)["tier"]


class ScorerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tiers = {s: tier(s) for s in itertools.product(range(4), repeat=4)}

    def test_every_combination_returns_a_known_tier(self):
        self.assertEqual(len(self.tiers), 256)
        self.assertLessEqual(set(self.tiers.values()), set(RANK))

    def test_raising_a_factor_never_lowers_the_tier(self):
        for scores, result in self.tiers.items():
            for i in range(4):
                if scores[i] < 3:
                    higher = scores[:i] + (scores[i] + 1,) + scores[i + 1:]
                    self.assertGreaterEqual(RANK[self.tiers[higher]], RANK[result], (scores, higher))

    def test_top_consequence_is_never_fast(self):
        for scores, result in self.tiers.items():
            if scores[2] == 3:
                self.assertNotEqual(result, "FAST", scores)

    def test_top_capability_is_reasoning(self):
        for scores, result in self.tiers.items():
            if scores[3] == 3:
                self.assertEqual(result, "REASONING", scores)

    def test_sum_thresholds(self):
        self.assertEqual(self.tiers[(1, 1, 1, 0)], "FAST")
        self.assertEqual(self.tiers[(1, 1, 1, 1)], "STANDARD")
        self.assertEqual(self.tiers[(2, 2, 2, 1)], "STANDARD")
        self.assertEqual(self.tiers[(2, 2, 2, 2)], "REASONING")

    def test_deterministic_flag_wins(self):
        self.assertEqual(tier((3, 3, 3, 3), "--deterministic"), "NO_LLM")

    def test_out_of_range_and_missing_arguments_are_rejected(self):
        self.assertEqual(run((4, 0, 0, 0)).returncode, 2)
        self.assertEqual(subprocess.run([sys.executable, str(SCORER)], capture_output=True).returncode, 2)


if __name__ == "__main__":
    unittest.main()
