#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
curl -L --fail --retry 3 -A 'Mozilla/5.0' 'https://video-s.twimg.com/amplify_video/2096970070283128833/vid/avc1/1920x1080/AFYuwiRiFVAlzB5o.mp4?tag=29' -o dist/source.mp4
python -m pip install --quiet faster-whisper
python process-temp-video.py
cat > dist/index.html <<'EOF'
<!doctype html><meta charset="utf-8"><title>xvid transcript bridge</title><a href="/transcript.json">transcript.json</a>
EOF
ls -lh dist/source.mp4 dist/transcript.json
