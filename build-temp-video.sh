#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
curl -L --fail --retry 3 -A 'Mozilla/5.0' 'https://video-s.twimg.com/amplify_video/2096970070283128833/vid/avc1/1920x1080/AFYuwiRiFVAlzB5o.mp4?tag=29' -o dist/source.mp4
python -m pip install --quiet faster-whisper imageio-ffmpeg requests
python process-temp-video.py
printf 'ok' > dist/index.html
ls -lh dist/source.mp4 dist/video-ja.mp4
