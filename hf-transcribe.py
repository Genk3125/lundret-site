import json, traceback
from pathlib import Path
OUT=Path('dist'); OUT.mkdir(exist_ok=True)
VIDEO='https://video-s.twimg.com/amplify_video/2096970070283128833/vid/avc1/1920x1080/AFYuwiRiFVAlzB5o.mp4?tag=29'
try:
    from gradio_client import Client, handle_file
    client=Client('YouLearn/faster-whisper', verbose=False)
    try:
        api_info=client.view_api(return_format='dict')
        (OUT/'api-info.json').write_text(json.dumps(api_info, ensure_ascii=False, default=str, indent=2), encoding='utf-8')
    except Exception as e:
        (OUT/'api-info.txt').write_text(f'{type(e).__name__}: {e}', encoding='utf-8')
    errors=[]; result=None
    for api in ['/transcribe','/predict']:
        try:
            result=client.predict(handle_file(VIDEO), 'small.en', api_name=api)
            break
        except Exception as e:
            errors.append(f'{api}: {type(e).__name__}: {e}')
    if result is None:
        (OUT/'hf-errors.txt').write_text('\n'.join(errors), encoding='utf-8')
    else:
        if not isinstance(result, str): result=json.dumps(result, ensure_ascii=False)
        (OUT/'transcript.json').write_text(result, encoding='utf-8')
except Exception:
    (OUT/'hf-errors.txt').write_text(traceback.format_exc(), encoding='utf-8')
