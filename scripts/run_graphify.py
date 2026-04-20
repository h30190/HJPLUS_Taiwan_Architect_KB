#!/usr/bin/env python3
"""Script to run graphify and auto-commit if output changed."""
import subprocess
import sys

# Run graphify
result = subprocess.run([sys.executable, 'graphify.py', './raw', '-o', './graphify-out'], capture_output=True, text=True)
print(result.stdout)
if result.stderr:
    print(result.stderr, file=sys.stderr)

# Check if graphify-out/ files changed
diff_result = subprocess.run(['git', 'diff', '--quiet', '--', 'graphify-out/'], capture_output=True)

# If files changed, add and commit them
if diff_result.returncode != 0:
    subprocess.run(['git', 'add', 'graphify-out/'])
    subprocess.run(['git', 'commit', '-m', 'chore: auto-update knowledge graph [skip ci]'], capture_output=True)

sys.exit(0)
