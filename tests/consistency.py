"""Runs /model-gate several times per sample intent and reports how often the tier agrees.

Each run starts a headless Claude Code session, so this spends tokens.
Run: python3 tests/consistency.py [runs-per-intent]
"""
import collections
import concurrent.futures
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/intent-driven-training"
INTENTS = sorted((ROOT / "tests/intents").glob("*.md"))
RUNS = int(sys.argv[1]) if len(sys.argv) > 1 else 3


def gate(intent):
    out = subprocess.run(
        ["claude", "--plugin-dir", str(PLUGIN), "-p", f"/intent-driven-training:model-gate {intent.name}",
         "--allowedTools", "Read,Glob,Grep,Bash", "--output-format", "json"],
        cwd=intent.parent, capture_output=True, text=True, stdin=subprocess.DEVNULL)
    result = json.loads(out.stdout)
    match = re.search(r"Recommended tier:\s*(\w+)", result.get("result") or "")
    return intent.name, match.group(1) if match else "UNPARSED", result.get("total_cost_usd", 0), result.get("duration_ms", 0)


jobs = [i for i in INTENTS for _ in range(RUNS)]
with concurrent.futures.ThreadPoolExecutor(6) as pool:
    rows = list(pool.map(gate, jobs))

by_intent = collections.defaultdict(list)
for name, tier, _, _ in rows:
    by_intent[name].append(tier)
agree = 0
for name, tiers in by_intent.items():
    agree += len(set(tiers)) == 1
    print(f"{name:28} {' '.join(tiers)}")
print(f"\n{agree}/{len(by_intent)} intents got the same tier on all {RUNS} runs")
print(f"mean cost ${sum(r[2] for r in rows) / len(rows):.3f}, mean time {sum(r[3] for r in rows) / len(rows) / 1000:.1f}s per run")
