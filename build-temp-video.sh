#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
curl -L --fail --retry 3 -A 'Mozilla/5.0' 'https://video-s.twimg.com/amplify_video/2096970070283128833/vid/avc1/1920x1080/AFYuwiRiFVAlzB5o.mp4?tag=29' -o dist/video.mp4
cat > dist/index.html <<'EOF'
<!doctype html>
<html><head><meta charset="utf-8"><title>Soshi xvid209697 preview</title></head>
<body><h1>Soshi xvid209697 preview</h1><a href="/video.mp4">video.mp4</a></body></html>
EOF
