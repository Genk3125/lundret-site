#!/usr/bin/env bash
set -u
mkdir -p dist
if python -m pip install --quiet gradio_client 2>dist/pip-errors.txt; then
  python hf-transcribe.py || true
else
  printf 'gradio_client install failed\n' > dist/hf-errors.txt
fi
cat > dist/index.html <<'EOF'
<!doctype html><meta charset="utf-8"><title>xvid transcript bridge</title>
<a href="/transcript.json">transcript</a> <a href="/hf-errors.txt">errors</a> <a href="/api-info.json">api</a> <a href="/pip-errors.txt">pip</a>
EOF
find dist -maxdepth 1 -type f -printf '%f %s\n' | sort > dist/files.txt
exit 0
