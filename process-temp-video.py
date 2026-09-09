import json
from pathlib import Path
from faster_whisper import WhisperModel

OUT = Path('dist')
video = OUT / 'source.mp4'
model = WhisperModel('tiny.en', device='cpu', compute_type='int8')
segments, info = model.transcribe(str(video), vad_filter=True, beam_size=1)
rows = []
for s in segments:
    text = s.text.strip()
    if text:
        rows.append({'start': round(s.start, 3), 'end': round(s.end, 3), 'en': text})
(OUT / 'transcript.json').write_text(json.dumps({'language': info.language, 'duration': info.duration, 'segments': rows}, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({'segments': len(rows), 'duration': info.duration}))
