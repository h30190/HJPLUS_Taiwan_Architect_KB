#!/bin/sh
# Run graphify and only commit if output changed
python graphify.py ./raw -o ./graphify-out

# Check if graphify-out/ files changed
git diff --quiet -- graphify-out/ && exit 0

# Files changed, add them
git add graphify-out/

# Commit the changes
git commit -m "chore: auto-update knowledge graph [skip ci]" 2>/dev/null || true

# Exit successfully
exit 0
