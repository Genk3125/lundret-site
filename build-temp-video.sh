#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
python -m pip install --quiet gradio_client
python hf-transcribe.py
cat > dist/index.html <<'EOF'
<!doctype html><meta charset="utf-8"><title>xvid transcript bridge</title><a href="/transcript.json">transcript.json</a>
EOF
ls -lh dist/transcript.json
