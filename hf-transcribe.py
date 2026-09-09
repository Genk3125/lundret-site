import json
from pathlib import Path
from gradio_client import Client, handle_file

VIDEO='https://video-s.twimg.com/amplify_video/2096970070283128833/vid/avc1/1920x1080/AFYuwiRiFVAlzB5o.mp4?tag=29'
OUT=Path('dist'); OUT.mkdir(exist_ok=True)
client=Client('YouLearn/faster-whisper', verbose=False)
errors=[]
result=None
for api in ['/transcribe','/predict']:
    try:
        result=client.predict(handle_file(VIDEO), 'small.en', api_name=api)
        break
    except Exception as e:
        errors.append(f'{api}: {type(e).__name__}: {e}')
if result is None:
    (OUT/'hf-errors.txt').write_text('\n'.join(errors), encoding='utf-8')
    raise RuntimeError('\n'.join(errors))
if not isinstance(result, str):
    result=json.dumps(result, ensure_ascii=False)
(OUT/'transcript.json').write_text(result, encoding='utf-8')
print(result[:2000])
