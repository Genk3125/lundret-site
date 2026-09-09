#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
curl -L --fail --retry 3 -A 'Mozilla/5.0' 'https://video-s.twimg.com/amplify_video/2096970070283128833/vid/avc1/1920x1080/AFYuwiRiFVAlzB5o.mp4?tag=29' -o dist/video.mp4
printf 'ok' > dist/index.html
ls -lh dist/video.mp4
